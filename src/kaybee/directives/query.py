from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util import logging

from kaybee.widgets.query import Query


class query(nodes.General, nodes.Element):
    @property
    def name(self):
        n = self.get('names')
        if n:
            return n[0]
        return None


class QueryDirective(Directive):
    has_content = True

    def run(self):
        # Get the info from this directive and make instance
        content = '\n'.join(self.content)
        this_query = Query(content)

        # TODO If the config says to validate, validate
        site = self.state.document.settings.env.site
        site.validator.validate(this_query)
        site.add_widget(this_query)

        # Now add the node to the doctree
        query_node = query()
        query_node.update_basic_atts(dict(names=[this_query.name]))
        return [query_node]
