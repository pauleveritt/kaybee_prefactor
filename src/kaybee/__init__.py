from kaybee.base_kb import kb
from kaybee.events import (
    kaybee_context,
    initialize_site,
    call_purge_doc,
    validate_references,
    missing_reference,
    generate_debug_info,
    builder_init,
    register_directives,
    generate_feeds,
    call_env_before_read_docs
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

    app.connect('builder-inited', builder_init)

    app.connect('env-purge-doc', call_purge_doc)

    app.connect('env-before-read-docs', initialize_site)

    app.connect('env-before-read-docs', call_env_before_read_docs)
    app.connect('env-before-read-docs', register_directives)

    app.connect('missing-reference', missing_reference)

    app.connect('env-check-consistency', validate_references)

    app.connect('env-check-consistency', generate_debug_info)

    app.connect('html-collect-pages', generate_feeds)

    app.connect('html-page-context', kaybee_context)

    return dict(
        version=__version__,
        parallel_read_safe=False
    )
