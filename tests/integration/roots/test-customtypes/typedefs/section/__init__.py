from kaybee.core.core_type import CoreContainerModel
from kaybee.core.registry import registry
from kaybee.resources import BaseResource


@registry.resource('section')
class Section(BaseResource):
    model = CoreContainerModel
