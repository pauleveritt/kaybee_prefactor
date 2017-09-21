from kaybee.resources import BaseResource


class Article(BaseResource):
    @property
    def navmenu_href(self):
        return self.name + '.html'
