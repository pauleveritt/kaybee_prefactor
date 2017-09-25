from docutils import nodes
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder


def process_query_nodes(app: Sphinx, doctree, fromdocname):
    """ Callback registered with Sphinx's doctree-resolved event """
    # Setup a template and context
    builder: StandaloneHTMLBuilder = app.builder
    site = app.env.site

    from kaybee.widgets import widget

    for node in doctree.traverse(widget):
        # Render the output
        widget = site.widgets.get(node.widget_name)
        context = builder.globalcontext.copy()
        context['site'] = site
        output = widget.render(builder, context, site)

        # Put the output into the node contents
        listing = [nodes.raw('', output, format='html')]
        node.replace_self(listing)
