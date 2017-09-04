from typing import List

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.util import logging

from ruamel.yaml import load

logger = logging.getLogger(__name__)


class QueryNode(nodes.General, nodes.Element):
    @staticmethod
    def load(content):
        """ Provide a way to stub this in tests """

        # If the string of YAML is empty-ish (new lines, etc.)
        # then return an empty dict
        if content.strip() == '':
            return {}
        return load(content)


class QueryDirective(Directive):
    has_content = True

    # option_specs = dict(
    #     rtype=directives.unicode_code,
    #     limit=directives.positive_int
    # )

    def run(self) -> List[QueryNode]:
        query_node = QueryNode('\n'.join(self.content))
        self.state.nested_parse(self.content, self.content_offset, query_node)
        return [query_node]


def process_query_nodes(app: Sphinx, doctree, fromdocname):

    # Setup a template and context
    builder: StandaloneHTMLBuilder = app.builder
    ctx = builder.globalcontext.copy()
    templatename = 'query.html'

    for node in doctree.traverse(QueryNode):

        # Get the YAML string, parse/validate it
        content = node.children[0].rawsource
        props = node.load(content)

        # Query the "database" based on props in the YAML
        resources = app.env.site.all_resources
        ctx['query_results'] = resources

        # Pass the results into Jinja2
        output = builder.templates.render(templatename, ctx)

        # Replace the rendered node contents with raw HTML
        listing = [nodes.raw('', output, format='html')]
        node.replace_self(listing)
