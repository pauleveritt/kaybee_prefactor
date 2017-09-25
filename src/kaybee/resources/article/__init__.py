from kaybee.decorators import kb
from kaybee.resources import BaseResource


@kb.resource('article')
class Article(BaseResource):
    @property
    def navmenu_href(self):
        return self.name + '.html'
