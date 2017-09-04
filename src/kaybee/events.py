"""
Choosing a Template - Precedence Rules
======================================

1. ``resource.template`` on the instance (in YAML)

2. Resource.template on the class

3. ``doc_template`` or ``listing_template`` in the config.section

4. If on the homepage, ``homepage.html``

5. If on any other page, ``page.html``

"""

from kaybee.site import Site


def initialize_site(app, env, docnames):
    """ Create the Site instance if it is not in the pickle """

    if not hasattr(env, 'site'):
        config = app.config.html_context['kaybee_config']
        env.site = Site(config)


def purge_resources(app, env, docname):
    if hasattr(env, 'site'):
        env.site.remove(docname)


def kb_context(app, pagename, templatename, context, doctree):

    site = app.env.site
    context['site'] = site

    ########################
    # Armageddon...this sucks, looks like articles/index as a pagename
    # and storing at "articles" in the site isn't going to be a good idea
    ########################

    pname = pagename
    if pagename.endswith('/index'):
        pname = pagename[:-6]
    resource = site.get(pname)

    if resource:
        # We return a custom template
        context['resource'] = resource
        context['parents'] = resource.parents(site)
        context['template'] = resource.template(site)
        return resource.template(site)

    else:
        return templatename