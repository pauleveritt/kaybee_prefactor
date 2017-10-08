from kaybee.core.core_type import CoreResourceModel
from kaybee.core.registry import registry
from kaybee.resources import BaseResource


class CategoryModel(CoreResourceModel):
    label: str


@registry.resource('article')
class Category(BaseResource):
    model = CategoryModel

    @property
    def navmenu_href(self):
        return self.name + '.html'
