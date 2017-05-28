"""
Implement a Page content type that can render itself
"""
from markupsafe import Markup

from kaybee.rms import CMS


class Page:
    """ The current file that is being rendered. """
    resource_type = 'Page'
    template = 'page.html'

    def __init__(self, site, resource, body: str):
        # The resource is the YAML data, the body is what Sphinx
        # renders into HTML
        self.site = site
        self.resource = resource
        self.body = body

    def active(self, nav_id):
        """ Determine if current resource is in a given sitenav section """
        section = self.resource.get('section')
        return 'active' if section == nav_id else ''

    def __call__(self):
        template = self.site.env.get_template('page.html')
        return template.render(page=self, site=self.site)


if __name__ == '__main__':
    cms = CMS('Some Sphinx docs site')
    resource1 = dict(
        title='Resource Page 1',
        subtitle='RP1 is subtitled',
        resource_type='Page',
        section='Home'
    )
    body = Markup('<p>This is the body</p>')
    this_page = cms.render(
        body,
        resource1
    )
    print(this_page())
