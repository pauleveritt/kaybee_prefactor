import os
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


def convert_path(path, pagename):
    # The config file's sections have an path. It is probably like
    # '/blog/'. Sphinx page names will be something like 'blog/index'
    # or 'blog/folder1/somedoc'. Return either None (the pagename is
    # not in the section, 'index' (the pagename is the index page for the
    # section, 'home' (the pagename is 'index'), or 'doc'
    # (the pagename is somewhere under the section.

    if not pagename.startswith(path):
        # This page is not in this section
        return None
    else:
        if pagename == 'index':
            # This is the home page
            return 'home'
        elif pagename == os.path.normpath(path + '/index'):
            return 'index'
        else:
            return 'doc'


def choose_layout_info(sections, pagename, kb_template=None):
    """ Return the section and template for this page """

    result = dict(style='', template='page', active='')
    for section in sections:
        page_type = convert_path(section['path'], pagename)
        if page_type is None:
            # No match
            continue

        # Set the style, template, and bail out of the loop
        if pagename == 'index':
            # This is the home page, it gets special styling
            result['style'] = 'header-image is-medium'
        else:
            result['style'] = 'is-bold is-%s' % section.get('color', '')

        if page_type == 'home':
            # The template for the homepage is either:
            result['template'] = section.get('doc_template', 'homepage')
        elif page_type == 'index':
            # If the config overrides the section template, use it
            result['template'] = section.get('listing_template',
                                             'section')
        else:
            # Leaf pages can get template from: config section,
            # a default to page.html, or below with the override
            result['template'] = section.get('doc_template', 'page')

        # In all cases, if this document has an override at the top,
        # then use it
        if kb_template:
            result['template'] = kb_template

        # Set this section as the active one, stripping out any
        # leading/trailing slashes
        result['active'] = [i for i in section['path'].split('/') if i][0]

        # We matched, bail on for loop and return
        return result

    return result


def kb_context(app, pagename, templatename, context, doctree):
    config = app.config.html_context['kaybee_config']

    # Find out which kind of page component this is, if meta even exists
    kb_template = context.get('meta', {}).get('kb_context')
    context['kb_context'] = kb_template

    layout_info = choose_layout_info(config['sections'], pagename,
                                     kb_template)
    context['kb_section_style'] = layout_info['style']
    context['kb_template'] = layout_info['template']
    context['kb_active_section'] = layout_info['active']

    template = layout_info['template']
    if template is not None:
        return template + '.html'


def setup(app):
    app.connect('html-page-context', kb_context)
    return dict(
        version=__version__,
        parallel_read_safe=True
    )
