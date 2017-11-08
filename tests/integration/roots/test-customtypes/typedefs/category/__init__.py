from kaybee.registry import registry
from kaybee.resources.base import BaseResourceModel, BaseResource


class CategoryModel(BaseResourceModel):
    label: str


@registry.resource('category')
class Category(BaseResource):
    model = CategoryModel

    @property
    def label(self):
        return self.props.label
