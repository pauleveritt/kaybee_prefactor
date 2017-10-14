import json
from datetime import datetime
from typing import List, Any, Mapping

from pydantic.main import BaseModel
from ruamel.yaml import load


class CorePropFilterModel(BaseModel):
    key: str
    value: Any


class CoreQueryModel(BaseModel):
    kbtype: str = None
    limit: int = 5
    parent_name: str = None
    sort_value: str = None
    order: int = None
    props: List[CorePropFilterModel] = []


class ReferencesType(str):
    @classmethod
    def get_validators(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, list):
            raise ValueError(f'reference: expected list, not {type(v)}')
        for i in v:
            if not isinstance(i, str):
                prefix = 'reference: expected list of strings, '
                msg = f'{prefix} not {type(i)}'
                raise ValueError(msg)
        return v


class CoreResourceModel(BaseModel):
    """ Kaybee default schema definitions for resources """

    template: str = None
    style: str = None
    in_nav: bool = False
    weight: int = 0
    synopsis: str = None
    published: datetime = None
    category: ReferencesType = []
    tag: ReferencesType = []


class CoreContainerModel(CoreResourceModel):
    """ A resource that is a parent for other resources

     Parents can override child properties based on kbtype

    E.g.

    overrides:
        article:
            template: customtemplate.html
            style: boldestbaddest

     """
    overrides: Mapping[str, Mapping[str, str]] = None


class CoreWidgetModel(BaseModel):
    template: str


class CoreType:
    model: BaseModel
    kind: str  # BaseResource and BaseWidget need to fill this in

    def __init__(self, docname: str, kbtype: str, yaml_content: str):
        # Raise custom exception if subclass doesn't have a model attr
        if not hasattr(self, 'model'):
            msg = f'Class {self.__class__.__name__} must have model attribute'
            raise AttributeError(msg)

        self.docname = docname
        self.parent = self.parse_parent(docname)
        self.name = self.get_name(yaml_content)
        self.kbtype = kbtype
        self.props = self.load_model(self.model, yaml_content)

    def get_name(self, yaml_content: str):
        """ The identifier that this instance is stored as """

        if self.kind == 'widget':
            # Resources use the docname, widgets will do something else,
            # since you might have multiple widgets per page
            yaml_props = (load(yaml_content) or {})
            return json.dumps(yaml_props, sort_keys=True)
        else:
            return self.docname

    @staticmethod
    def load_model(model, yaml_content: str):
        # If yaml_content is an empty string and parses to None, return
        # empty dic instead
        yaml_props = (load(yaml_content) or {})

        # Make the model, which validates, then do any extra validation
        m = model(**yaml_props)
        return m

    @staticmethod
    def parse_parent(docname):
        """ Given a docname path, pick apart and return name of parent """

        lineage = docname.split('/')
        lineage_count = len(lineage)

        if docname == 'index':
            # This is the top of the Sphinx project
            parent = None
        elif lineage_count == 1:
            # This is a non-index doc in root, e.g. about
            parent = 'index'
        elif lineage_count == 2 and lineage[-1] == 'index':
            # This is blog/index, parent is the root
            parent = 'index'
        elif lineage_count == 2:
            # This is blog/about
            parent = lineage[0] + '/index'
        elif lineage[-1] == 'index':
            # This is blog/sub/index
            parent = '/'.join(lineage[:-2]) + '/index'
        else:
            # This should be blog/sub/about
            parent = '/'.join(lineage[:-1]) + '/index'

        return parent
