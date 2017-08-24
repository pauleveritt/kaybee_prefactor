import os

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


def kb_template(app, pagename, templatename, context, doctree):
    config = app.config.html_context

    # Need some info about the "section" of the site
    if pagename.startswith('blog'):
        section_style = 'is-bold is-warning'
    elif pagename.startswith('articles'):
        section_style = 'is-bold is-info'
    elif pagename.startswith('tutorials'):
        section_style = 'is-bold is-light'
    elif pagename.startswith('about'):
        section_style = 'is-bold is-success'
    else:
        section_style = 'header-image is-medium'
    context['kb_section_style'] = section_style

    # Find out which kind of page component this is, if meta even exists
    kb_template = context.get('meta', {}).get('kb_template')
    context['kb_template'] = kb_template

    if kb_template:
        # We have RST page with the magic marker at the top. Return
        # this as the template name. Later, do more sniffing.
        return kb_template + '.html'


def setup(app):
    app.connect('html-page-context', kb_template)
    return dict(
        version=__version__,
        parallel_read_safe=True
    )
