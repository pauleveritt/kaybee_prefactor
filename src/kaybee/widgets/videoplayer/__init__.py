from pydantic.main import BaseModel

from kaybee.core.registry import registry
from kaybee.widgets.base import BaseWidget


class VideoPlayerModel(BaseModel):
    width: int = 640
    height: int = 360
    src: str
    frameborder: int = 0
    allowfullscreen: bool = True


@registry.widget('videoplayer')
class VideoPlayer(BaseWidget):
    model = VideoPlayerModel
    template = 'videoplayer.html'
