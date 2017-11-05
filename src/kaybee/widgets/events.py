from docutils import nodes
from sphinx.addnodes import toctree
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.environment import BuildEnvironment

from kaybee.core.site import Site
from kaybee.widgets.node import widget


def process_widget_nodes(app: Sphinx, doctree, fromdocname):
    """ Callback registered with Sphinx's doctree-resolved event """
    # Setup a template and context
    builder: StandaloneHTMLBuilder = app.builder
    env: BuildEnvironment = app.env
    site: Site = env.site

    if app.config.kaybee_config.use_toctree:
        from kaybee.widgets.kbtoctree import KbToctree
        for node in doctree.traverse(toctree):
            if node.attributes['hidden']:
                continue

            w = KbToctree()
            context = builder.globalcontext.copy()
            context['site'] = site

            # The challenge here is that some items in a toctree
            # might not be resources in our "database". So we have
            # to ask Sphinx to get us the titles.
            w.set_entries(node.attributes['entries'], env.titles, site.resources)
            output = w.render(builder, context, site)

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
