from kaybee.base_types import CoreResourceModel
from kaybee.registry import registry
from kaybee.resources.base import BaseArticle


class ArticleModel(CoreResourceModel):
    flag: int = None


@registry.resource('article')
class Article(BaseArticle):
    model = ArticleModel
