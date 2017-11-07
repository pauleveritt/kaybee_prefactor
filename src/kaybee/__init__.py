from kaybee.events import (
    kaybee_context, add_templates_paths,
    initialize_site, purge_resources,
    validate_references,
    missing_reference,
    generate_debug_info,
    builder_init
)
from kaybee.site_config import SiteConfig

__version__ = "0.0.1"

__title__ = "kaybee"
__description__ = "Knowledge base system for Sphinx"
__uri__ = "https://github.com/pauleveritt/kaybee"
__doc__ = __description__ + " <" + __uri__ + ">"

__author__ = "Paul Everitt"
__email__ = "pauleveritt@me.org"

__license__ = "Apache License 2.0"
__copyright__ = "Copyright (c) 2017 Paul Everitt"


def setup(app):
    app.add_config_value('kaybee_config', SiteConfig(), 'html')

    app.connect('builder-inited', builder_init)
    app.connect('builder-inited', add_templates_paths)

    app.connect('env-purge-doc', purge_resources)

    app.connect('env-before-read-docs', initialize_site)

    app.connect('missing-reference', missing_reference)

    app.connect('env-check-consistency', validate_references)

    app.connect('env-check-consistency', generate_debug_info)

    app.connect('html-page-context', kaybee_context)

    return dict(
        version=__version__,
        parallel_read_safe=False
    )
