"""

Use a Sphinx-style setup function to register all of our resource
type handlers.

"""
from kaybee.resources.page import Page
from kaybee.rms import CMS


@CMS.render.register(resource_type='Page')
def render_page(cms, page_body, resource=Page):
    page1 = Page(
        cms,
        resource,
        body=page_body
    )
    return page1


def setup(app):
    return