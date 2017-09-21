from docutils import nodes
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder

from kaybee.directives.query import query, QueryDirective
from kaybee.directives.resource import ResourceDirective


def process_query_nodes(app: Sphinx, doctree, fromdocname):
    """ Callback registered with Sphinx's doctree-resolved event """
    # Setup a template and context
    builder: StandaloneHTMLBuilder = app.builder
    site = app.env.site

    for node in doctree.traverse(query):
        # Render the output
        widget = site.widgets.get(node.name)
        context = builder.globalcontext.copy()
        context['site'] = site
        output = widget.render(builder, context, site)

        # Put the output into the node contents
        listing = [nodes.raw('', output, format='html')]
        node.replace_self(listing)


def setup(app):
    # Resource directive
    app.add_directive('resource', ResourceDirective)

    # Query support
    app.add_node(query)
    app.add_directive('query', QueryDirective)
    app.connect('doctree-resolved', process_query_nodes)
