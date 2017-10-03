from kaybee.core.registry import registry
from kaybee.resources import BaseResource


@registry.resource('homepage')
class Homepage(BaseResource):
    default_style = 'header-image is-medium'
