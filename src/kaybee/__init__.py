import inspect
import os

import dectate
import importscan
from sphinx.jinja2glue import SphinxFileSystemLoader

import kaybee
from kaybee import directives
from kaybee import resources, widgets
from kaybee.decorators import kb
from kaybee.events import kb_context

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


def add_templates_paths(app):
    """ Add the kaybee template directories

     Using Sphinx's conf.py support for registering new template
     directories is both cumbersome and, for us, wrong. We don't
     want to do it at import time. Instead, we want to do it at
     Dectate-configure time.
     """

    template_bridge = app.builder.templates

    # Add the root of kaybee, then add the widgets and resources
    f = os.path.join(os.path.dirname(inspect.getfile(kaybee)), 'templates')
    template_bridge.loaders.append(SphinxFileSystemLoader(f))
    items = sorted(kb.config.widgets.items()) + \
            sorted(kb.config.resources.items())
    for k, v in items:
        f = os.path.dirname(inspect.getfile(v))
        template_bridge.loaders.append(SphinxFileSystemLoader(f))


def setup(app):
    importscan.scan(resources)
    importscan.scan(widgets)
    dectate.commit(kb)
    app.connect('builder-inited', add_templates_paths)
    app.connect('env-before-read-docs', events.initialize_site)
    app.connect('env-purge-doc', events.purge_resources)
    app.connect('html-page-context', kb_context)

    # Delegate directive registration
    directives.setup(app)

    return dict(
        version=__version__,
        parallel_read_safe=True
    )
