from kaybee.core.core_type import CoreResourceModel
from kaybee.core.registry import registry
from kaybee.resources import BaseResource


class CategoryModel(CoreResourceModel):
    label: str


@registry.resource('category')
class Category(BaseResource):
    model = CategoryModel

    @property
    def navmenu_href(self):
        return self.name + '.html'

    @property
    def label(self):
        """ Enable reference behavior

         Implementing this allows this resource to be indexed as a
         "reference" using the return-value label as a shorthand
         pointer to this resource. E.g. ref:category:thislabel

         By default, return the title. It's expected that the RST
         title matches the shorthand label.
         """

        return self.props.label
