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

import dectate
import importscan
from pykwalify.core import Core
from ruamel.yaml import load_all
from sphinx.jinja2glue import SphinxFileSystemLoader

import kaybee
from kaybee import resources, widgets
from kaybee.core.decorators import kb
from kaybee.site import Site


def _load_typedef(full_fn):
    """ Given a fn of YAML, parse it and configure registry """

    typeinfo_path = os.path.join(
        os.path.dirname(inspect.getfile(kaybee)),
        'core/typeinfo.yaml'
    )
    with open(full_fn, 'r') as f:
        content = f.read()
        typeinfo, schema = list(load_all(content))

        # Validate the typeinfo, which has to conform to a schema
        c = Core(source_data=typeinfo, schema_files=[typeinfo_path])
        c.validate(raise_exception=True)


def register(app):
    """ Load the resources, types, etc. from the registry

    We can get resources etc. from 3 location: classes in kaybee itself,
    classes in the doc project, and YAML "typedef" files in the doc
    project.
    """

    # If the site has a kaybee_config, get it
    kc = app.config.kaybee_config
    if kc:
        # First the typedefs.yaml files in the doc project
        typedefs = kc.get('typedefs')
        if typedefs:
            for typedef_fn in typedefs:
                full_fn = os.path.join(app.confdir, typedef_fn)
                assert os.path.exists(full_fn)
                _load_typedef(full_fn)

    # Finally, scan for decorators in kaybee core
    importscan.scan(resources)
    importscan.scan(widgets)

    dectate.commit(kb)

    # Once config is setup, use it to drive various Sphinx registrations
    # (nodes, directives)
    resources.setup(app)
    widgets.setup(app)


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


def initialize_site(app, env, docnames):
    """ Create the Site instance if it is not in the pickle """

    if not hasattr(env, 'site'):
        config = app.config.html_context
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
