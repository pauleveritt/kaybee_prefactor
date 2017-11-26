from kaybee import kb
from kaybee.resources.base import BaseContainerModel, BaseResource


@kb.resource('section')
class Section(BaseResource):
    model = BaseContainerModel
