import os

from kaybee.events import kb_context
from kaybee import directives

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


def get_html_templates_path():
    """Return path to theme's template folder.

    Used by the doc project's config.py to hook into the template
    setup where templates are under the project root.
    """

    pkgdir = os.path.abspath(os.path.dirname(__file__))
    rtypes = ('article', 'section', 'homepage')
    types_dir = [os.path.join(pkgdir, 'resources', r) for r in rtypes]
    templates_dir = [
        os.path.join(pkgdir, 'templates'),
        os.path.join(pkgdir, 'directives/templates'),
    ]
    return templates_dir + types_dir


def setup(app):
    app.connect('env-before-read-docs', events.initialize_site)
    app.connect('env-purge-doc', events.purge_resources)
    app.connect('html-page-context', kb_context)

    # Delegate directive registration
    directives.setup(app)

    return dict(
        version=__version__,
        parallel_read_safe=True
    )
