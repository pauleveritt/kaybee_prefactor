from kaybee.core.registry import registry
from kaybee.resources import BaseResource


@registry.resource('blogpost')
class Blogpost(BaseResource):

    @property
    def navmenu_href(self):
        return self.name + '.html'
