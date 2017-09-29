import json
from collections import Mapping

from docutils import nodes
from docutils.parsers.rst import Directive
from ruamel.yaml import load

from kaybee.core.decorators import kb
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

    def run(self):
        """ Run at parse time.

        When the documents are initially being scanned, this method runs
        and does two things: (a) creates an instance that is added to
        the site's widgets, and (b) leaves behind a placeholder docutils
        node that can later be processed after the docs are resolved.
        The latter needs enough information to retrieve the former.

        """

        # Get the info from this directive and make instance
        wtype = self.name
        widget_content = '\n'.join(self.content)
        widget_class = kb.config.widgets[wtype]
        this_widget = widget_class(widget_content)
        this_widget.wtype = wtype

        # Validate the properties against the schema for this
        # widget type
        site = self.state.document.settings.env.site
        site.validator.validate(this_widget)
        site.add_widget(this_widget)

        # Now add the node to the doctree
        widget_node = widget()
        attrs = dict(ids=[this_widget.name], names=[wtype])
        widget_node.update_basic_atts(attrs)
        return [widget_node]


class BaseWidget:
    wtype = None

    def __init__(self, content):
        self.content = content
        self.props = self.load(content)

    @classmethod
    def set_wtype(cls, wtype):
        """ Stamp the wtype on the class at config time.

         The kb decorator has the name of the directive. The
         widget class needs to know the name of that directive
         to register itself. Help dectate registration to
         stamp the wtype on the class.
         """

        cls.wtype = wtype

    @staticmethod
    def load(content):
        """ Provide a way to stub this in tests """

        # If the string of YAML is empty-ish (new lines, etc.)
        # then return an empty dict
        if content.strip() == '':
            return {}
        return load(content)

    @property
    def template(self):
        """ Allow the template used to come from different places """

        # For now, it comes from a mandatory item in the YAML
        return self.props['template']

    @property
    def name(self):
        """ Generate a stable, re-usable identifier

         We need a key to store this instance on the site. We don't
         want to make the author's concoct some unique id to add
         in the YAML in the .rst file. Also, if the same widget is
         used in more than one place, we might want to cache the
         results.

         Generate a key as a string from the JSON representation of the
         sorted properties.
         """

        return json.dumps(self.props, sort_keys=True)

    def make_context(self, context: Mapping, site):
        raise NotImplementedError('Subclass must override make_context')

    def render(self, builder, context, site):
        """ Given a Sphinx builder and context with site in it,
         generate HTML """

        context['site'] = site
        self.make_context(context, site)
        # NOTE: Can use builder.templates.render_string
        html = builder.templates.render(self.template, context)
        return html


def setup(app):
    # Loop through the registered widgets and add a directive
    # for each
    app.add_node(widget)
    for w in kb.config.widgets.values():
        app.add_directive(w.wtype, BaseDirective)

    app.connect('doctree-resolved', process_widget_nodes)
