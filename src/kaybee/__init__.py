from kaybee.base_kb import kb
from kaybee.events import (
    kaybee_context,
    call_purge_doc,
    call_env_check_consistency,
    call_missing_reference,
    call_builder_init,
    call_env_before_read_docs,
    call_doctree_read,
    call_doctree_resolved,
    call_html_collect_pages
)
from kaybee.siteconfig import SiteConfig

__version__ = "0.0.3"

__title__ = "kaybee"
__description__ = "Knowledge base system for Sphinx"
__uri__ = "https://github.com/pauleveritt/kaybee"
__doc__ = __description__ + " <" + __uri__ + ">"

__author__ = "Paul Everitt"
__email__ = "pauleveritt@me.org"

__license__ = "Apache License 2.0"
__copyright__ = "Copyright (c) 2017 Paul Everitt"


def setup(app):
    app.config['template_bridge'] = 'kaybee.template_bridge.KaybeeBridge'

    app.add_config_value('kaybee_config', SiteConfig(), 'html')

    app.connect('builder-inited', call_builder_init)

    app.connect('env-purge-doc', call_purge_doc)

    app.connect('env-before-read-docs', call_env_before_read_docs)

    app.connect('doctree-read', call_doctree_read)
    app.connect('doctree-resolved', call_doctree_resolved)

    app.connect('missing-reference', call_missing_reference)

    app.connect('env-check-consistency', call_env_check_consistency)

    app.connect('html-collect-pages', call_html_collect_pages)

    app.connect('html-page-context', kaybee_context)

    return dict(
        version=__version__,
        parallel_read_safe=False
    )
