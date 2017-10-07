from kaybee.core.core_type import CoreResourceModel
from kaybee.core.registry import registry
from kaybee.resources import BaseResource


class HomepageModel(CoreResourceModel):
    logo: str = None
    style = 'header-image is-medium'


@registry.resource('homepage')
class Homepage(BaseResource):
    model = HomepageModel
