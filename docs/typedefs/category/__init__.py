from kaybee.core.core_type import CoreResourceModel
from kaybee.core.registry import registry
from kaybee.resources import BaseResource


class CategoryModel(CoreResourceModel):
    label: str


@registry.resource('category')
class Category(BaseResource):
    model = CategoryModel

    @property
    def label(self):
        return self.props.label
