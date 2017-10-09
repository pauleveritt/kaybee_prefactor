from docutils import nodes
from sphinx.addnodes import toctree
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder


def process_widget_nodes(app: Sphinx, doctree, fromdocname):
    """ Callback registered with Sphinx's doctree-resolved event """
    # Setup a template and context
    builder: StandaloneHTMLBuilder = app.builder
    site = app.env.site

    from kaybee.widgets import widget

    # for n in doctree.traverse(toctree):
    #     entries = [e[1] for e in n.attributes['entries']]
    #     x = n.asdom().toprettyxml()
    #
    for node in doctree.traverse(widget):
        # Render the output
        widget = site.widgets.get(node.name)
        context = builder.globalcontext.copy()
        context['site'] = site
        output = widget.render(builder, context, site)

        # Put the output into the node contents
        listing = [nodes.raw('', output, format='html')]
        node.replace_self(listing)
