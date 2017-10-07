from kaybee.core.core_type import CoreContainerModel
from kaybee.core.registry import registry
from kaybee.resources import BaseResource


class SectionModel(CoreContainerModel):
    subheading: str = None


@registry.resource('section')
class Section(BaseResource):
    model = SectionModel
    pass
