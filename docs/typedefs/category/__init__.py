from kaybee.base_types import CoreResourceModel
from kaybee.registry import registry
from kaybee.resources import BaseResource


class CategoryModel(CoreResourceModel):
    label: str


@registry.resource('category')
class Category(BaseResource):
    model = CategoryModel

    @property
    def label(self):
        return self.props.label
