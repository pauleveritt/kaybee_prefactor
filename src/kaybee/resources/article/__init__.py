from kaybee.core.core_type import CoreResourceModel
from kaybee.core.registry import registry
from kaybee.resources import BaseResource


class ArticleModel(CoreResourceModel):
    pass


@registry.resource('article')
class Article(BaseResource):
    model = ArticleModel

    def series(self, site):
        parent = site.resources[self.parent]
        results = []
        for docname in parent.toctree:
            resource = site.resources[docname]
            results.append(
                dict(
                    docname=docname,
                    title=resource.title,
                    synopsis=resource.props.synopsis
                )
            )
        return results
