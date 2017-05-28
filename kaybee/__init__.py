import os

from kaybee import _version as version
from kaybee.rms import CMS
from kaybee.sample_data import sample_site
from kaybee.resources import setup

cms = CMS(sample_site['title'], config={})
cms.is_sphinx = True
setup(sample_site['sphinx_config'])


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

    resource = sample_site['items'][0]['resource']
    body = context.get('body')

    context['page'] = cms.render(
        body,
        resource
    )
    context['site'] = cms


def setup(app):
    app.connect('html-page-context', update_context)
    return {'version': version.__version__,
            'parallel_read_safe': True}
