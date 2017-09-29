from kaybee.core.decorators import kb
from kaybee.resources import BaseResource


@kb.resource('article')
class Article(BaseResource):

    @property
    def navmenu_href(self):
        return self.name + '.html'


@kb.site()
class Site:
    name = 'Bubba Palace'
