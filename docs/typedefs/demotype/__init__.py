from kaybee.registry import registry
from kaybee.resources.base import BaseResourceModel, BaseResource


class DemoTypeModel(BaseResourceModel):
    flag: int = None


@registry.resource('demotype')
class DemoType(BaseResource):
    model = DemoTypeModel
