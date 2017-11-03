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
            resource = site.resources.get(docname)
            if resource:
                # We might have a non-resource page in the toctree,
                # so skip it if true
                synopsis = getattr(resource.props, 'synopsis', False)
                results.append(
                    dict(
                        docname=docname,
                        title=resource.title,
                        synopsis=synopsis
                    )
                )
        return results
