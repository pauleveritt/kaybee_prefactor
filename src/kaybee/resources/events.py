from pathlib import PurePath

from docutils.nodes import document
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment

from kaybee.core.site import Site


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

    # Get the title out of the RST and assign to the resource
    if resource:
        title = doctree.children[0].children[0].rawsource
        resource.title = title
    else:
        # This is a genericpage
        pass