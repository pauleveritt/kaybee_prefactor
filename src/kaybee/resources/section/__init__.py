from kaybee.core.core_type import CoreResourceModel
from kaybee.core.registry import registry
from kaybee.resources import BaseResource


class SectionModel(CoreResourceModel):
    subheading: str = None
    doc_template: str = None


@registry.resource('section')
class Section(BaseResource):
    model = SectionModel
    pass
