from kaybee.core.core_type import CoreResourceModel
from kaybee.core.registry import registry
from kaybee.resources.base import BaseArticle


class ArticleModel(CoreResourceModel):
    flag: int = None


@registry.resource('article')
class Article(BaseArticle):
    model = ArticleModel
