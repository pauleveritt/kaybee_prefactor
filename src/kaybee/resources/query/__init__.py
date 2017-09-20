from docutils import nodes
from ruamel.yaml import load
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder

from kaybee.directives import query


class Query:
    """ Model stored in the site with the parameters for this query """

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


    @staticmethod
    def process_query_nodes(app: Sphinx, doctree, fromdocname):
        """ Callback registered with Sphinx's doctree-resolved event """
        # Setup a template and context
        builder: StandaloneHTMLBuilder = app.builder
        ctx = builder.globalcontext.copy()
        templatename = 'query.html'

        for node in doctree.traverse(query):
            # Get the YAML string, parse/validate it
            content = node.children[0].rawsource
            props = node.load(content)

            # Query the "database" based on props in the YAML
            resources = app.env.site.filter_resources(**props)
            ctx['query_results'] = resources

            # Pass the results into Jinja2
            output = builder.templates.render(templatename, ctx)

            # Replace the rendered node contents with raw HTML
            listing = [nodes.raw('', output, format='html')]
            node.replace_self(listing)
