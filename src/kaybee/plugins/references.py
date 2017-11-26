from kaybee import kb
from kaybee.resources.base import BaseResourceModel, BaseResource


class BaseReferenceModel(BaseResourceModel):
    label: str


class BaseReference(BaseResource):
    model = BaseReferenceModel
    is_reference = True


@kb.event('env-before-read-docs', 'references')
def register_references(kb, app, env, docnames):
    """ Walk the registry and add sphinx directives """

    site = env.site

    for name, klass in kb.config.resources.items():
        # Name is the value in the decorator and directive, e.g.
        # @kb.resource('category') means name=category
        if getattr(klass, 'is_reference', False):
            site.references[name] = dict()


def setup(app):
    """ Wire up Sphinx events """
    return
    # app.connect('env-before-read-docs', register_references)
