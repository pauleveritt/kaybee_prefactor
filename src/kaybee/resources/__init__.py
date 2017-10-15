from kaybee.resources.base import BaseResource
from kaybee.core.registry import registry
from kaybee.resources.directive import BaseResourceDirective
from kaybee.resources.events import (
    doctree_read_resources
)


def setup(app):
    # Loop through the registered resources and add a directive
    # for each
    for kbtype in registry.config.resources.keys():
        app.add_directive(kbtype, BaseResourceDirective)

    app.connect('doctree-read', doctree_read_resources)
