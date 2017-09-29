import os

import dectate
import importscan

import kaybee
from kaybee import resources, widgets
from kaybee.core.decorators import kb
from kaybee.events import kb_context, add_templates_paths, initialize_site

__version__ = "0.0.1"

__title__ = "kaybee"
__description__ = "Knowledge base system for Sphinx"
__uri__ = "https://github.com/pauleveritt/kaybee"
__doc__ = __description__ + " <" + __uri__ + ">"

__author__ = "Paul Everitt"
__email__ = "pauleveritt@me.org"

__license__ = "Apache License 2.0"
__copyright__ = "Copyright (c) 2017 Paul Everitt"


def get_path():
    """
    Called from the entry point in setup.py
    """
    # Theme directory is defined as our parent directory
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def setup(app):
    importscan.scan(resources)
    importscan.scan(widgets)
    dectate.commit(kb)
    app.connect('builder-inited', add_templates_paths)
    app.connect('env-before-read-docs', initialize_site)
    app.connect('env-purge-doc', events.purge_resources)
    app.connect('html-page-context', kb_context)

    # Delegate directive registration
    resources.setup(app)
    widgets.setup(app)

    return dict(
        version=__version__,
        parallel_read_safe=True
    )
