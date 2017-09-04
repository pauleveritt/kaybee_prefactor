from docutils.parsers.rst import Directive


class ResourceDirective(Directive):
    has_content = True
    required_arguments = 1

    def run(self):
        env = self.state.document.settings.env
        rtype = self.arguments[0]
        # There has to be a better way than this. Requires that
        # the directive be placed after the rst title
        title = self.state.parent.parent.children[0].children[0].rawsource
        block = '\n'.join(self.content)
        klass = env.site.get_class(rtype)
        resource = klass(env.docname, rtype, title, block)

        # TODO If the config says to validate, validate
        resource.validate(resource.props, resource.schema)
        env.site.add(resource)
        return []
