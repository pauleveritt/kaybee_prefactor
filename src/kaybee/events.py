import os

from kaybee.site import Site


def initialize_site(app, env, docnames):
    """ Create the Site instance if it is not in the pickle """

    if not hasattr(env, 'site'):
        env.site = Site()


def purge_resources(app, env, docname):
    if hasattr(env, 'site'):
        env.site.remove(docname)


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
    context['kb_active_section'] = layout_info['active']

    template = layout_info['template']

    site = app.env.site
    context['site'] = site
    resource = site.get(pagename)

    if resource:
        context['resource'] = resource
        context['parents'] = resource.parents(site)
        context['kb_template'] = resource.template + '.html'
        return resource.template + '.html'

    elif template is not None:
        context['kb_template'] = layout_info['template']
        return template + '.html'
