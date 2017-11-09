from kaybee.registry import registry
from kaybee.resources.base import BaseResourceModel, BaseResource


class ArticleModel(BaseResourceModel):
    flag: int = None


@registry.resource('article')
class Article(BaseResource):
    model = ArticleModel
