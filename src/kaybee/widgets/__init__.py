import inspect
import os
from collections import Mapping

from docutils import nodes
from docutils.parsers.rst import Directive
from ruamel.yaml import load

from kaybee.core.core_type import CoreType
from kaybee.core.registry import registry
from kaybee.widgets.events import process_widget_nodes


class widget(nodes.General, nodes.Element):
    """ Generic invisible node that goes in doctree.

     When parsing doctrees, we might stumble across, in the middle
     of a document, a widget. The doctree needs a node that can
     be converted to a site.widgets[name] reference. Stick a
     generic, invisible (nothing rendered to output) node in the
     document, then extract (a) the kind of widget (classname) and
     (b) the identifier for the particular widget.

     """

    @property
    def name(self):
        """ This is the identifier for this node """

        return self['ids'][0]

    @property
    def kbtype(self):
        """ The directive used, which finds the class needed

         If our RST has ``.. querylist::``
         """

        n = self.get('names', None)
        if n:
            return n[0]
        return None


class BaseWidgetDirective(Directive):
    has_content = True

    @classmethod
    def get_widget_class(cls, widget_directive):
        """ Make this easy to mock """
        return registry.config.widgets[widget_directive]

    # @property
    # def doc_title(self):
    #     return self.state.parent.parent.children[0].children[0].rawsource

    def get_widget(self, docname):
        # Get the info from this directive and make instance
        kbtype = self.name
        widget_content = '\n'.join(self.content)
        widget_class = BaseWidgetDirective.get_widget_class(kbtype)
        return widget_class(
            docname,
            kbtype, widget_content
        )

    def run(self):
        """ Run at parse time.

        When the documents are initially being scanned, this method runs
        and does two things: (a) creates an instance that is added to
        the site's widgets, and (b) leaves behind a placeholder docutils
        node that can later be processed after the docs are resolved.
        The latter needs enough information to retrieve the former.

        """

        env = self.state.document.settings.env
        this_widget = self.get_widget(env.docname)

        env.site.widgets[this_widget.name] = this_widget

        # Now add the node to the doctree
        widget_node = widget()
        attrs = dict(ids=[this_widget.name], names=[self.name])
        widget_node.update_basic_atts(attrs)
        return [widget_node]


class BaseWidget(CoreType):
    kind = 'widget'

    @property
    def template(self):
        """ Allow the template used to come from different places """

        # For now, it comes from a mandatory item in the YAML
        return self.props.template

    def make_context(self, context: Mapping, site):
        pass

    def render(self, builder, context, site):
        """ Given a Sphinx builder and context with site in it,
         generate HTML """

        context['site'] = site
        context['widget'] = self

        # make_context is optionally implemented on the concrete class
        # for each widget
        self.make_context(context, site)

        # NOTE: Can use builder.templates.render_string
        html = builder.templates.render(self.template, context)
        return html

    @classmethod
    def get_schema(cls):
        """ Subclasses or instances can override this """
        class_name = cls.__name__.lower()
        class_filename = inspect.getfile(cls)
        package_dir = os.path.dirname(class_filename)
        schema_filename = os.path.join(package_dir, class_name + '.yaml')
        with open(schema_filename, 'r') as f:
            schema = load(f)
            return schema


def setup(app):
    # Loop through the registered widgets and add a directive
    # for each
    app.add_node(widget)
    for kbtype in registry.config.widgets.keys():
        app.add_directive(kbtype, BaseWidgetDirective)

    app.connect('doctree-resolved', process_widget_nodes)
