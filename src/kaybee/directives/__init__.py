from kaybee.directives.events import process_query_nodes
from kaybee.directives.query import query, QueryDirective
from kaybee.directives.resource import ResourceDirective


def setup(app):
    # Resource directive
    app.add_directive('resource', ResourceDirective)

    # Query support
    app.add_node(query)
    app.add_directive('query', QueryDirective)
    app.connect('doctree-resolved', process_query_nodes)
