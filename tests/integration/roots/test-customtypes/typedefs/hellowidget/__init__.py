from pydantic.main import BaseModel

from kaybee import kb
from kaybee.widgets.base import BaseWidget


class HelloWidgetModel(BaseModel):
    flag: int = 100


@kb.widget('hellowidget')
class HelloWidget(BaseWidget):
    model = HelloWidgetModel
    template = 'hellowidget.html'
