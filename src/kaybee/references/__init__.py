from kaybee.resources.base import BaseResourceModel, BaseResource


class BaseReferenceModel(BaseResourceModel):
    label: str


class BaseReference(BaseResource):
    model = BaseReferenceModel


def setup(app):
    """ Wire up Sphinx events """
    pass
