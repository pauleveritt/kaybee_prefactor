from kaybee.core.core_type import CoreResourceModel
from kaybee.core.registry import registry
from kaybee.resources import BaseResource


class HomepageModel(CoreResourceModel):
    logo: str = None


@registry.resource('homepage')
class Homepage(BaseResource):
    model = HomepageModel
    default_style = 'header-image is-medium'
