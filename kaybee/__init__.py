import os

# from kaybee.fake_kaybee_api import Page, Site, Sphinx
from kaybee import _version as version


def get_path():
    """
    Shortcut for users whose theme is next to their conf.py.
    """
    # Theme directory is defined as our parent directory
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def get_html_templates_path():
    """Return path to theme's template folder.

    Used by the doc project's config.py to hook into the template 
    setup.
    """

    pkgdir = os.path.abspath(os.path.dirname(__file__))
    return [os.path.join(pkgdir, 'templates')]


def update_context(app, pagename, templatename, context, doctree):
    context['theme_version'] = version.__version__
    # context['page'] = Page(body=context.get('body'))
    # context['site'] = Site()
    # context['sphinx'] = Sphinx(is_sphinx=True)


def setup(app):
    app.connect('html-page-context', update_context)
    return {'version': version.__version__,
            'parallel_read_safe': True}
