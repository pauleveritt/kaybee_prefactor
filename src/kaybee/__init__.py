import os

from events import kb_context

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
    return [os.path.join(pkgdir, 'templates')]


def setup(app):
    app.connect('html-page-context', kb_context)
    return dict(
        version=__version__,
        parallel_read_safe=True
    )
