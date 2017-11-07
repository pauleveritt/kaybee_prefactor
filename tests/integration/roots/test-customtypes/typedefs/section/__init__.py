from kaybee.base_types import CoreContainerModel
from kaybee.registry import registry
from kaybee.resources import BaseResource


@registry.resource('section')
class Section(BaseResource):
    model = CoreContainerModel
