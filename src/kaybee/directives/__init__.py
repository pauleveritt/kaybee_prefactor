from kaybee.directives.query import QueryNode, Query, process_query_nodes
from kaybee.directives.resource import ResourceDirective


def setup(app):
    # Resource directive
    app.add_directive('resource', ResourceDirective)

    # Query support
    app.add_node(QueryNode)
    app.add_directive('query', Query)
    app.connect('doctree-resolved', process_query_nodes)
