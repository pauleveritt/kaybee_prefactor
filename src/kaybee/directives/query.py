from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util import logging

from kaybee.resources.query import Query

logger = logging.getLogger(__name__)


class query(nodes.General, nodes.Element):
    @property
    def name(self):
        n = self.get('names')
        if n:
            return n[0]
        return None


class QueryDirective(Directive):
    has_content = True
    required_arguments = 1

    def run(self):
        # Get the info from this directive and make instance
        name = self.arguments[0]
        content = '\n'.join(self.content)
        this_query = Query(name, content)

        # TODO If the config says to validate, validate
        site = self.state.document.settings.env.site
        site.validator.validate(this_query)
        site.add(this_query)

        # Now add the node to the doctree
        query_node = query()
        query_node.update_basic_atts(dict(names=[name]))
        return [query_node]
