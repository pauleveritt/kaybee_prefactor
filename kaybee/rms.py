"""

Wrapper for the "Site" and the registration system.

"""
import reg
from jinja2 import Environment, PackageLoader, select_autoescape


class CMS:
    is_sphinx = False

    def __init__(self, title, config):
        # The config comes from the Sphinx conf.py file
        self.title = title
        self.env = Environment(
            loader=PackageLoader('kaybee', 'templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        self.config = config

    @reg.dispatch_method(
        reg.match_key(
            'resource_type',
            lambda self, body, resource: resource.get('resource_type'))
    )
    def render(self, body, resource):
        raise NotImplementedError

    def pathto(self, fn, flag):
        """ Simulate sphinx's pathto function """

        if self.is_sphinx:
            newfn = fn  ##[1:]  # _static -> static
        else:
            newfn = fn[1:]  # _static -> static
        return newfn
