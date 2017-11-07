from kaybee.base_types import CoreResourceModel
from kaybee.registry import registry
from kaybee.resources import BaseResource


class DemoTypeModel(CoreResourceModel):
    flag: int = None


@registry.resource('demotype')
class DemoType(BaseResource):
    model = DemoTypeModel
