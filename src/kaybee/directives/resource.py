from docutils.parsers.rst import Directive


class ResourceDirective(Directive):
    has_content = True
    required_arguments = 1

    def run(self):
        env = self.state.document.settings.env
        site = env.site

        rtype = self.arguments[0]
        # There has to be a better way than this. Requires that
        # the directive be placed after the rst title
        title = self.state.parent.parent.children[0].children[0].rawsource
        block = '\n'.join(self.content)
        klass = site.get_class(rtype)
        this_resource = klass(env.docname, rtype, title, block)

        # TODO If the config says to validate, validate
        site.validator.validate(this_resource)
        site.add_resource(this_resource)

        # Don't need to return a resource "node", the
        # document is the node
        return []
