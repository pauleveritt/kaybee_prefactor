import inspect
import json
from collections import Mapping

import os
from docutils import nodes
from docutils.parsers.rst import Directive
from ruamel.yaml import load

from kaybee.core.core_type import CoreType
from kaybee.core.registry import registry
from kaybee.core.validators import validate
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
    def wtype(self):
        """ The directive used, which finds the class needed

         If our RST has ``.. querylist::``
         """

        n = self.get('names', None)
        if n:
            return n[0]
        return None


class BaseDirective(Directive):
    has_content = True

    @classmethod
    def get_widget_schema(cls, kbtype):
        """ Make this easy to mock """
        return registry.first_action('widget', kbtype)

    def validate_widget(self, widget, kbtype):
        props = widget.props
        action_data = self.get_widget_schema(kbtype)
        schema_data = action_data.schema
        validate(props, schema_data)

    def run(self):
        """ Run at parse time.

        When the documents are initially being scanned, this method runs
        and does two things: (a) creates an instance that is added to
        the site's widgets, and (b) leaves behind a placeholder docutils
        node that can later be processed after the docs are resolved.
        The latter needs enough information to retrieve the former.

        """

        # Get the info from this directive and make instance
        kbtype = self.name
        widget_content = '\n'.join(self.content)
        widget_class = registry.config.widgets[kbtype]
        this_widget = widget_class(widget_content)
        this_widget.wtype = kbtype

        # Validate the properties against the schema for this
        # widget type
        # TODO 001 No longer the site's responsibility
        self.validate_widget(this_widget, kbtype)
        site = self.state.document.settings.env.site
        site.add_widget(this_widget)

        # Now add the node to the doctree
        widget_node = widget()
        attrs = dict(ids=[this_widget.name], names=[kbtype])
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
        raise NotImplementedError('Subclass must override make_context')

    def render(self, builder, context, site):
        """ Given a Sphinx builder and context with site in it,
         generate HTML """

        context['site'] = site

        # make_context is implemented on the concrete class for each widget
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
        # TODO 001 Have the registry interact with Sphinx and do this?
        app.add_directive(kbtype, BaseDirective)

    app.connect('doctree-resolved', process_widget_nodes)
