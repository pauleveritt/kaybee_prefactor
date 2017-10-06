from kaybee.core.core_type import CoreResourceModel
from kaybee.core.registry import registry
from kaybee.resources import BaseResource


class BlogpostModel(CoreResourceModel):
    flag: int = None


@registry.resource('blogpost')
class Blogpost(BaseResource):
    model = BlogpostModel

    @property
    def navmenu_href(self):
        return self.name + '.html'
