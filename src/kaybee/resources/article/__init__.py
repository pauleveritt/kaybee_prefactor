from kaybee.core.core_type import CoreResourceModel
from kaybee.core.registry import registry
from kaybee.resources import BaseResource


class ArticleModel(CoreResourceModel):
    pass


@registry.resource('article')
class Article(BaseResource):
    model = ArticleModel

    @property
    def navmenu_href(self):
        return self.name + '.html'
