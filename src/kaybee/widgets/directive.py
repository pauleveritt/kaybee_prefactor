from docutils.parsers.rst import Directive

from kaybee.registry import registry
from kaybee.widgets.node import widget


class BaseWidgetDirective(Directive):
    has_content = True

    @classmethod
    def get_widget_class(cls, widget_directive):
        """ Make this easy to mock """
        return registry.config.widgets[widget_directive]

    def get_widget(self, docname):
        # Get the info from this directive and make instance
        kbtype = self.name
        widget_content = '\n'.join(self.content)
        widget_class = BaseWidgetDirective.get_widget_class(kbtype)
        return widget_class(docname, kbtype, widget_content)

    @property
    def docname(self):
        """ Easier to mock by abstracting Sphinx environment """

        return self.state.document.settings.env.docname

    @property
    def widgets(self):
        """ Easier to mock by abstracting Sphinx environment """

        env = self.state.document.settings.env
        return env.site.widgets

    def run(self):
        """ Run at parse time.

        When the documents are initially being scanned, this method runs
        and does two things: (a) creates an instance that is added to
        the site's widgets, and (b) leaves behind a placeholder docutils
        node that can later be processed after the docs are resolved.
        The latter needs enough information to retrieve the former.

        """

        this_widget = self.get_widget(self.docname)

        self.widgets[this_widget.name] = this_widget

        # Now add the node to the doctree
        widget_node = widget()
        attrs = dict(ids=[this_widget.name], names=[self.name])
        widget_node.update_basic_atts(attrs)
        return [widget_node]
