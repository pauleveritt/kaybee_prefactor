import datetime
import inspect
import json
import os

import dectate
from docutils import nodes
from sphinx.jinja2glue import SphinxFileSystemLoader

from kaybee import resources, widgets, references
from kaybee.registry import registry
from kaybee.resources.directive import BaseResourceDirective
from kaybee.site import Site
from kaybee.widgets.directive import BaseWidgetDirective


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


def builder_init(app):
    """ On the builder init event, commit registry and pass setup """
    dectate.commit(registry)
    resources.setup(app)
    widgets.setup(app)
    references.setup(app)


def purge_resources(app, env, docname):
    if hasattr(env, 'site'):
        # TODO need to remove widgets when the document has one
        env.site.resources.pop(docname, None)


def add_templates_paths(app, env, docnames):
    """ Add the kaybee template directories

     Using Sphinx's conf.py support for registering new template
     directories is both cumbersome and, for us, wrong. We don't
     want to do it at import time. Instead, we want to do it at
     Dectate-configure time.
     """

    template_bridge = app.builder.templates

    # Add _templates in the conf directory
    confdir = os.path.join(app.confdir, '_templates')
    template_bridge.loaders.append(SphinxFileSystemLoader(confdir))

    # Add the widgets and resources
    values = list(registry.config.widgets.values()) + \
             list(registry.config.resources.values()) + \
             list(registry.config.cores.values())

    for v in values:
        f = os.path.dirname(inspect.getfile(v))
        template_bridge.loaders.append(SphinxFileSystemLoader(f))


def initialize_site(app, env, docnames):
    """ Create the Site instance if it is not in the pickle """

    if not hasattr(env, 'site'):
        config = getattr(app.config, 'kaybee_config')
        if config:
            env.site = Site(config)


def register_directives(app, env, docnames):
    """ Walk the registry and add sphinx directives """

    for kbtype in registry.config.resources.keys():
        app.add_directive(kbtype, BaseResourceDirective)

    for kbtype in registry.config.widgets.keys():
        app.add_directive(kbtype, BaseWidgetDirective)


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
                    assert srfn[target_label].props.label == target_label
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


def generate_debug_info(builder, env):
    """ html-collect-pages event to dump some JSON to a file """

    site = env.site

    if not getattr(site.config, 'is_debug'):
        return

    debug = dict()
    qr = dectate.Query('resource')
    qw = dectate.Query('widget')
    debug['registry'] = dict(
        resources=[i[0].name for i in list(qr(registry))],
        widgets=[i[0].name for i in list(qw(registry))],
    )

    # Navmenu
    nm = [nm.docname for nm in site.navmenu]

    # Resources
    r = {
        k: v.to_json(site)
        for (k, v) in site.resources.items()
    }

    # Widgets
    w = {
        k: v.to_json(site)
        for (k, v) in site.widgets.items()
    }
    debug['site'] = dict(
        navmenu=nm,
        resources=r,
        widgets=w,
        pages=[p.docname for p in env.site.genericpages.values()]
    )

    # Write info
    output_filename = os.path.join(builder.outdir, 'debug_dump.json')
    with open(output_filename, 'w') as f:
        json.dump(debug, f, default=datetime_handler)


def kaybee_context(app, pagename, templatename, context, doctree):
    site = app.env.site
    context['site'] = site

    resource = site.resources.get(pagename)

    dectate.commit(registry)

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
        # Should have a genericpage in the dict
        genericpage = site.genericpages.get(pagename)
        if genericpage:
            context['page'] = genericpage
            return genericpage.template()

    return templatename
