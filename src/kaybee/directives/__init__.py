from kaybee.directives.events import process_query_nodes
from kaybee.directives.querylist import querylist, QueryListDirective
from kaybee.directives.resource import ResourceDirective


def setup(app):
    # Resource directive
    app.add_directive('resource', ResourceDirective)

    # Query support
    app.add_node(querylist)
    app.add_directive('querylist', QueryListDirective)
    app.connect('doctree-resolved', process_query_nodes)
