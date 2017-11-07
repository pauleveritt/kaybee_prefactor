from pydantic.main import BaseModel

from kaybee.registry import registry
from kaybee.widgets.base import BaseWidget


class HelloWidgetModel(BaseModel):
    flag: int = 100


@registry.widget('hellowidget')
class HelloWidget(BaseWidget):
    model = HelloWidgetModel
    template = 'hellowidget.html'
