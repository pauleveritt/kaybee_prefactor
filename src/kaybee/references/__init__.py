from kaybee.references.events import register_references
from kaybee.resources.base import BaseResourceModel, BaseResource


class BaseReferenceModel(BaseResourceModel):
    label: str


class BaseReference(BaseResource):
    model = BaseReferenceModel
    is_reference = True


def setup(app):
    """ Wire up Sphinx events """
    app.connect('env-before-read-docs', register_references)
