from kaybee.registry import registry
from kaybee.resources.base import BaseArticle, BaseResourceModel


class ArticleModel(BaseResourceModel):
    flag: int = None


@registry.resource('article')
class Article(BaseArticle):
    model = ArticleModel
