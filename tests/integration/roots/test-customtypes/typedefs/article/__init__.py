from kaybee import kb
from kaybee.resources.base import BaseResourceModel, BaseResource


class ArticleModel(BaseResourceModel):
    flag: int = None


@kb.resource('article')
class Article(BaseResource):
    model = ArticleModel
