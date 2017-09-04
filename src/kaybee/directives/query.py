from typing import List

import sphinx
from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.util import logging

logger = logging.getLogger(__name__)

class QueryNode(nodes.General, nodes.Element):
    pass


class Query(Directive):
    has_content = False
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {}

    def run(self) -> List[QueryNode]:
        return [QueryNode()]


def process_query_nodes(app: Sphinx, doctree, fromdocname):
    builder: StandaloneHTMLBuilder = app.builder
    ctx = builder.globalcontext.copy()
    templatename = 'query.html'
    output = builder.templates.render(templatename, ctx)
    for node in doctree.traverse(QueryNode):
        listing = [nodes.raw('', output, format='html')]
        node.replace_self(listing)

