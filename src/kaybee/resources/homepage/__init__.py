from kaybee.decorators import kb
from kaybee.resources import BaseResource


@kb.resource('homepage')
class Homepage(BaseResource):
    directive_name = 'homepage'
    default_style = 'header-image is-medium'
