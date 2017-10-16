import inspect
import json
import os

import dectate
import importscan
from docutils import nodes
from sphinx.jinja2glue import SphinxFileSystemLoader

import kaybee
from kaybee import resources, widgets
from kaybee.core.registry import registry
from kaybee.core.site import Site


def register(app):
    """ Load the resources, types, etc. from the registry

    We can get resources etc. from 3 location: classes in kaybee itself,
    classes in the doc project, and YAML "typedef" files in the doc
    project.
    """

    # First, scan for decorators in kaybee core and commit
    importscan.scan(resources)
    importscan.scan(widgets)
    dectate.commit(registry)

    # If the site has a kaybee_config, get it
    kc = app.config.kaybee_config

    # TODO OO2 We are yanking this out
    # if kc:
    #     # First the typedefs.yaml files in the doc project
    #     typedefs = kc.get('typedefs')
    #     if typedefs:
    #         for typedef_fn in typedefs:
    #             full_fn = os.path.join(app.confdir, typedef_fn)
    #             assert os.path.exists(full_fn)
    #             yaml_typedef = YamlTypedef(full_fn)
    #             yaml_typedef.register(registry)

    dectate.commit(registry)

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
    values = list(registry.config.widgets.values()) + \
             list(registry.config.resources.values())
    for v in values:
        f = os.path.dirname(inspect.getfile(v))
        template_bridge.loaders.append(SphinxFileSystemLoader(f))


def initialize_site(app, env, docnames):
    """ Create the Site instance if it is not in the pickle """

    if not hasattr(env, 'site'):
        # Load and validate the config
        config = app.config.kaybee_config
        env.site = Site(config)


def purge_resources(app, env, docname):
    if hasattr(env, 'site'):
        # TODO need to remove widgets when the document has one
        env.site.resources.pop(docname, None)


def kaybee_context(app, pagename, templatename, context, doctree):
    site = app.env.site
    context['site'] = site

    resource = site.resources.get(pagename)

    # XXX TODO Make this debug stuff configurable
    dectate.commit(registry)
    debug = dict()
    qr = dectate.Query('resource')
    qw = dectate.Query('widget')
    debug['registry'] = dict(
        resources=[i[0].name for i in list(qr(registry))],
        widgets=[i[0].name for i in list(qw(registry))],
    )
    context['debug'] = json.dumps(debug)

    context['site_config'] = app.config.kaybee_config

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


def validate_references(app, env):
    """ Called on env-check-consistency, make sure references exist """

    site = env.site
    for resource in site.resources.values():
        for field_name in resource.reference_fieldnames:
            for target_label in getattr(resource.props, field_name):
                # Make sure this label exists in site.reference
                try:
                    srfn = site.references[field_name]
                except KeyError:
                    msg = f'''\
Document {resource.name} has unregistered reference "{field_name}"'''
                    raise KeyError(msg)
                try:
                    assert srfn[target_label].label == target_label
                except AssertionError:
                    msg = f'''\
Document {resource.name} has "{field_name}" with orphan {target_label} '''
                    raise KeyError(msg)


def missing_reference(app, env, node, contnode):
    site = env.site
    refdoc = node['refdoc']
    target_kbtype, target_label = node['reftarget'].split('-')
    target = site.get_reference(target_kbtype, target_label)

    if node['refexplicit']:
        # The ref has a title e.g. :ref:`Some Title <category-python>`
        dispname = contnode.children[0]
    else:
        # Use the title from the target
        dispname = target.title
    uri = app.builder.get_relative_uri(refdoc, target.name)
    newnode = nodes.reference('', '', internal=True, refuri=uri,
                              reftitle=dispname)

    emp = nodes.emphasis()
    newnode.append(emp)
    emp.append(nodes.Text(dispname))
    return newnode
