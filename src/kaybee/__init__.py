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


def choose_layout_info(sections, pagename, kb_template=None):
    """ Return the section and template for this page """

    result = dict(style='', template='page')
    if pagename == 'index':
        # Home page
        result['style'] = 'header-image is-medium'
        result['template'] = kb_template or 'homepage'
    else:
        for section in sections:
            if pagename.startswith(section['path']):
                # Set the color scheme
                result['style'] = 'is-bold is-%s' % section['color']

                # Is this the section listing?
                if pagename == section['path'] + '/index':
                    # If the config overrides the section template, use it
                    result['template'] = section.get('sectionpage_template',
                                                     'sectionpage')
                else:
                    # Leaf pages can get template from: config section,
                    # a default to page.html, or below with the override
                    result['template'] = section.get('template', 'page')

            # In all cases, if this document has an override at the top,
            # then use it
            if kb_template:
                result['template'] = kb_template

    return result


def kb_context(app, pagename, templatename, context, doctree):
    config = app.config.html_context

    # Find out which kind of page component this is, if meta even exists
    kb_template = context.get('meta', {}).get('kb_context')
    context['kb_context'] = kb_template

    layout_info = choose_layout_info(config['global_navigation'], pagename,
                                     kb_template)
    context['kb_section_style'] = layout_info['style']
    context['kb_template'] = layout_info['template']

    template = layout_info['template']
    if template is not None:
        return template + '.html'


def setup(app):
    app.connect('html-page-context', kb_context)
    return dict(
        version=__version__,
        parallel_read_safe=True
    )
