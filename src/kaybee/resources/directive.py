from docutils.parsers.rst import Directive

from kaybee.registry import registry


class BaseResourceDirective(Directive):
    has_content = True

    @classmethod
    def get_resource_class(cls, resource_directive):
        """ Make this easy to mock """
        return registry.config.resources[resource_directive]

    @property
    def docname(self):
        """ Easier to mock by abstracting Sphinx environment """

        return self.state.document.settings.env.docname

    @property
    def site(self):
        """ Easier to mock by abstracting Sphinx environment """

        return self.state.document.settings.env.site

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
        resource_content = '\n'.join(self.content)
        resource_class = BaseResourceDirective.get_resource_class(kbtype)
        this_resource = resource_class(self.docname, kbtype, resource_content)

        # Add this resource to the site
        self.site.resources[this_resource.name] = this_resource

        # If this is a reference, add it to site references
        if getattr(resource_class, 'is_reference', False):
            label = this_resource.props.label
            self.site.add_reference(kbtype, label, this_resource)

        # Don't need to return a resource "node", the
        # document is the node
        return []
