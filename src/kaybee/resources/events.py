from sphinx.addnodes import toctree
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment

from kaybee.site import Site


def process_resource_nodes(app: Sphinx, doctree, docname):
    """ Callback registered with Sphinx's  """

    env: BuildEnvironment = app.env
    site: Site = env.site

    resource = site.resources[docname]
    if resource:
        # Stamp the title on the node
        title = doctree.children[0].children[0].rawsource
        resource.title = title
    else:
        pass
