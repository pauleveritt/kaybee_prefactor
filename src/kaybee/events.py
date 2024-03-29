import os

import dectate
from docutils.nodes import document
from sphinx.application import Sphinx
from sphinx.jinja2glue import SphinxFileSystemLoader

from kaybee import kb
from kaybee.plugins.events import EventAction
from kaybee.site import Site


def call_builder_init(app):
    """ On the builder init event, commit registry and pass setup """
    dectate.commit(kb)


def call_purge_doc(app, env, docname):
    for callback in EventAction.get_callbacks(kb, 'env-purge-doc'):
        callback(kb, app, env, docname)


def call_env_before_read_docs(app, env, docnames):
    """ Single event handler which dispatches to kb events"""

    if not hasattr(env, 'site'):
        config = getattr(app.config, 'kaybee_config')
        if config:
            env.site = Site(config)

    template_bridge = app.builder.templates

    # Add _templates in the conf directory
    confdir = os.path.join(app.confdir, '_templates')
    template_bridge.loaders.append(SphinxFileSystemLoader(confdir))

    for callback in EventAction.get_callbacks(kb, 'env-before-read-docs'):
        callback(kb, app, env, docnames)


def call_doctree_read(app: Sphinx, doctree: document):
    for callback in EventAction.get_callbacks(kb, 'doctree-read'):
        callback(kb, app, doctree)


def call_doctree_resolved(app: Sphinx, doctree: document, fromdocname):
    for callback in EventAction.get_callbacks(kb, 'doctree-resolved'):
        callback(kb, app, doctree, fromdocname)


def call_html_collect_pages(app: Sphinx):
    for callback in EventAction.get_callbacks(kb, 'html-collect-pages'):
        return callback(kb, app)


def call_env_check_consistency(builder, env):
    for callback in EventAction.get_callbacks(kb, 'env-check-consistency'):
        return callback(kb, builder, env)


def call_missing_reference(app: Sphinx, env, node, contnode):
    for callback in EventAction.get_callbacks(kb, 'missing-reference'):
        return callback(kb, app, env, node, contnode)


def call_html_context(app, pagename, templatename, context, doctree):
    for callback in EventAction.get_callbacks(kb, 'html-context'):
        return callback(kb, app, pagename, templatename, context, doctree)
