from kaybee import kb
from kaybee.resources.base import BaseResourceModel, BaseResource


class DemoTypeModel(BaseResourceModel):
    flag: int = None


@kb.resource('demotype')
class DemoType(BaseResource):
    model = DemoTypeModel
