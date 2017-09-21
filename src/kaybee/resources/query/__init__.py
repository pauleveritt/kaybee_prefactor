from ruamel.yaml import load


class Query:
    """ Model stored in the site with the parameters for this query """

    template = 'query.html'
    rtype = 'query'  # TODO get rid of this

    def __init__(self, name, content):
        self.name = name  # This should be a unique ID
        self.props = Query.load(content)

    @staticmethod
    def load(content):
        """ Provide a way to stub this in tests """

        # If the string of YAML is empty-ish (new lines, etc.)
        # then return an empty dict
        if content.strip() == '':
            return {}
        return load(content)

    def render(self, builder, context):
        """ Given a Sphinx builder and context with site in it,
         generate HTML """

        site = context['site']
        context['results'] = site.filter_resources(**self.props)
        html = builder.templates.render(self.template, context)
        return html
