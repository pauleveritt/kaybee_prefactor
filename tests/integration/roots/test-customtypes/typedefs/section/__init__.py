from kaybee.registry import registry
from kaybee.resources.base import BaseContainerModel, BaseResource


@registry.resource('section')
class Section(BaseResource):
    model = BaseContainerModel
