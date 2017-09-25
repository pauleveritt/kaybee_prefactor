from kaybee.decorators import kb
from kaybee.resources import BaseResource


@kb.widget('homepage')
class Homepage(BaseResource):
    default_style = 'header-image is-medium'
