from kaybee.decorators import kb
from kaybee.resources import BaseResource


@kb.resource('section')
class Section(BaseResource):
    directive_name = 'section'
