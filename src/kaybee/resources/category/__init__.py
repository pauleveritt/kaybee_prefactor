from kaybee.core.core_type import CoreResourceModel
from kaybee.core.registry import registry
from kaybee.resources import BaseResource


class CategoryModel(CoreResourceModel):
    pass


@registry.resource('category')
class Category(BaseResource):
    model = CategoryModel

    @property
    def navmenu_href(self):
        return self.name + '.html'
