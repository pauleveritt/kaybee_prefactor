from docutils.parsers.rst import Directive

from kaybee.core.registry import registry


class BaseResourceDirective(Directive):
    has_content = True

    @classmethod
    def get_resource_class(cls, resource_directive):
        """ Make this easy to mock """
        return registry.config.resources[resource_directive]

    def run(self):
        """ Run at parse time.

        When the documents are initially being scanned, this method runs
        and does two things: (a) creates an instance that is added to
        the site's widgets, and (b) leaves behind a placeholder docutils
        node that can later be processed after the docs are resolved.
        The latter needs enough information to retrieve the former.

        """

        env = self.state.document.settings.env

        # Get the info from this directive and make instance
        kbtype = self.name
        resource_content = '\n'.join(self.content)
        resource_class = BaseResourceDirective.get_resource_class(kbtype)
        this_resource = resource_class(env.docname, kbtype, resource_content)

        # Add this to the site, and if it is a reference, index it
        site = self.state.document.settings.env.site
        site.resources[this_resource.name] = this_resource
        if hasattr(this_resource, 'label'):
            # This resource is a reference. Find all of the fields
            # that
            label = this_resource.label
            site.add_reference(kbtype, label, this_resource)

        # Don't need to return a resource "node", the
        # document is the node
        return []
