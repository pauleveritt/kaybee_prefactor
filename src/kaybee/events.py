"""
Choosing a Template - Precedence Rules
======================================

1. ``resource.template`` on the instance (in YAML)

2. Resource.template on the class

3. ``doc_template`` or ``listing_template`` in the config.section

4. If on the homepage, ``homepage.html``

5. If on any other page, ``page.html``

"""

import inspect
import os

from sphinx.jinja2glue import SphinxFileSystemLoader

import kaybee
from kaybee.decorators import kb
from kaybee.site import Site


def initialize_site(app, env, docnames):
    """ Create the Site instance if it is not in the pickle """

    if not hasattr(env, 'site'):
        config = app.config.html_context['kaybee_config']
        env.site = Site(config)


def purge_resources(app, env, docname):
    if hasattr(env, 'site'):
        # TODO need to remove widgets when the document has one
        env.site.remove_resource(docname)


def kb_context(app, pagename, templatename, context, doctree):
    site = app.env.site
    context['site'] = site

    ########################
    # Armageddon...this sucks, looks like articles/index as a pagename
    # and storing at "articles" in the site isn't going to be a good idea
    ########################

    pname = pagename
    if pagename.endswith('/index'):
        pname = pagename[:-6]
    resource = site.resources.get(pname)

    if resource:
        # We return a custom template
        context['resource'] = resource
        context['parents'] = resource.parents(site)
        context['template'] = resource.template(site)

        # Also, replace sphinx "title" with the title from this resource
        context['title'] = resource.title
        return resource.template(site)

    else:
        return templatename


def add_templates_paths(app):
    """ Add the kaybee template directories

     Using Sphinx's conf.py support for registering new template
     directories is both cumbersome and, for us, wrong. We don't
     want to do it at import time. Instead, we want to do it at
     Dectate-configure time.
     """

    template_bridge = app.builder.templates

    # Add the root of kaybee
    f = os.path.join(os.path.dirname(inspect.getfile(kaybee)), 'templates')
    template_bridge.loaders.append(SphinxFileSystemLoader(f))

    # Add _templates in the conf directory
    confdir = os.path.join(app.confdir, '_templates')
    template_bridge.loaders.append(SphinxFileSystemLoader(confdir))

    # Add the widgets and resources
    values = list(kb.config.widgets.values()) + \
             list(kb.config.resources.values())
    for v in values:
        f = os.path.dirname(inspect.getfile(v))
        template_bridge.loaders.append(SphinxFileSystemLoader(f))
