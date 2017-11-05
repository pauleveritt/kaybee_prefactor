from kaybee.core.core_type import CoreResourceModel
from kaybee.core.registry import registry
from kaybee.resources import BaseResource


class DemoTypeModel(CoreResourceModel):
    flag: int = None


@registry.resource('demotype')
class DemoType(BaseResource):
    model = DemoTypeModel
