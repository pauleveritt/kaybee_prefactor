from docutils import nodes
from sphinx.addnodes import toctree
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.environment import BuildEnvironment

from kaybee.site import Site
from kaybee.widgets.kbtoctree import KbToctree


def process_widget_nodes(app: Sphinx, doctree, fromdocname):
    """ Callback registered with Sphinx's doctree-resolved event """
    # Setup a template and context
    builder: StandaloneHTMLBuilder = app.builder
    env: BuildEnvironment = app.env
    site: Site = env.site

    from kaybee.widgets import widget

    for node in doctree.traverse(toctree):
        w = KbToctree()
        context = builder.globalcontext.copy()
        context['site'] = site

        titles = env.titles
        output = w.render(builder, context, site,
                          node, titles)

        # Put the output into the node contents
        listing = [nodes.raw('', output, format='html')]
        node.replace_self(listing)

    for node in doctree.traverse(widget):
        # Render the output
        w = site.widgets.get(node.name)
        context = builder.globalcontext.copy()
        context['site'] = site
        output = w.render(builder, context, site)

        # Put the output into the node contents
        listing = [nodes.raw('', output, format='html')]
        node.replace_self(listing)
