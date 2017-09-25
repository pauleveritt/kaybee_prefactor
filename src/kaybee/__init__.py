import os

from sphinx.jinja2glue import SphinxFileSystemLoader

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
    widgets = ('querylist',)
    types_dirs = [os.path.join(pkgdir, 'resources', r) for r in rtypes]
    widgets_dirs = [os.path.join(pkgdir, 'widgets', r) for r in widgets]
    templates_dir = [
        os.path.join(pkgdir, 'templates'),
        os.path.join(pkgdir, 'directives/templates'),
    ]
    return templates_dir + types_dirs + widgets_dirs


def add_templates_paths(app):
    """ Add the kaybee template directories

     Using Sphinx's conf.py support for registering new template
     directories is both cumbersome and, for us, wrong. We don't
     want to do it at import time.
     """
    template_paths = get_html_templates_path()
    template_bridge = app.builder.templates
    template_bridge.loaders += [SphinxFileSystemLoader(x) for x in
                                template_paths]


def setup(app):
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
