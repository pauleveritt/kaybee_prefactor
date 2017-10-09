from pydantic.main import BaseModel

from kaybee.core.registry import registry
from kaybee.widgets import BaseWidget


class KbToctreeModel(BaseModel):
    flag: int


@registry.widget('kbtoctree')
class KbToctree(BaseWidget):
    model = KbToctreeModel
    template = 'kbtoctree.html'
    is_toctree = True
