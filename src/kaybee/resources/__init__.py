from kaybee.resources.base import BaseResource
from kaybee.resources.directive import BaseResourceDirective
from kaybee.resources.events import (
    doctree_read_resources
)


def setup(app):
    app.connect('doctree-read', doctree_read_resources)
