from pathlib import PurePath

from docutils.nodes import document
from sphinx.addnodes import toctree
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment

from kaybee.registry import registry
from kaybee.site import Site


def doctree_read_resources(app: Sphinx, doctree: document):
    # Called during the 'doctree-read' Sphinx event
    env: BuildEnvironment = app.env
    site: Site = env.site

    confdir = app.confdir
    source = PurePath(doctree.attributes['source'])

    # Get the relative path inside the docs dir, without .rst, then
    # get the reource
    docname = str(source.relative_to(confdir)).split('.rst')[0]
    resource = site.resources.get(docname)

    # Get the class registered as the genericpage handler
    gp = registry.config.cores.get('genericpage')

    # Get the title out of the RST and assign to the resource
    if resource:
        # Step 1: Stamp the title on the resource
        title = doctree.children[0].children[0].rawsource
        resource.title = title

        # Step 2: Find any toctrees (at most one, hopefully) and record
        for node in doctree.traverse(toctree):
            resource.toctree = [
                target for (flag, target) in node.attributes['entries']
            ]
            pass

    else:
        # This is a genericpage
        if gp:
            genericpage = gp(docname)
            site.genericpages[docname] = genericpage
