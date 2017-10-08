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


class CoreResourceModel(BaseModel):
    """ Kaybee default schema definitions for resources """

    template: str = None
    style: str = None
    in_nav: bool = False
    weight: int = 0
    synopsis: str = None
    published: datetime = None


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

    def __init__(self, pagename: str, kbtype: str,
                 title: str, yaml_content: str):
        # Raise custom exception if subclass doesn't have a model attr
        if not getattr(self, 'model'):
            msg = f'Class {self.__class__.__name__} must have model attribute'
            raise AttributeError(msg)

        self.pagename, self.parent = self.parse_pagename(pagename)
        self.name = self.get_name(yaml_content)
        self.kbtype = kbtype
        self.title = title
        self.props = self.load_model(self.model, yaml_content)

    def get_name(self, yaml_content: str):
        """ The identifier that this instance is stored as """

        if self.kind == 'widget':
            # Resources use the pagename, widgets will do something else,
            # since you might have multiple widgets per page
            yaml_props = (load(yaml_content) or {})
            return json.dumps(yaml_props, sort_keys=True)
        else:
            return self.pagename

    @staticmethod
    def load_model(model, yaml_content: str):
        # If yaml_content is an empty string and parses to None, return
        # empty dic instead
        yaml_props = (load(yaml_content) or {})

        # Make the model, which validates, then do any extra validation
        m = model(**yaml_props)
        return m

    @staticmethod
    def parse_pagename(pagename):
        """ Instead of doing this in the constructor, more testable """

        lineage = pagename.split('/')
        lineage_count = len(lineage)

        # Default
        name = pagename

        if lineage_count == 1:
            # This is a doc in the root e.g. index or about
            parent = '/'
        elif lineage_count == 2 and lineage[-1] == 'index':
            # This is blog/index, parent is the root
            name = lineage[0]
            parent = '/'
        elif lineage_count == 2:
            # This is blog/about
            parent = lineage[0]
        elif lineage[-1] == 'index':
            # This is blog/sub/index
            name = '/'.join(lineage[:-1])
            parent = '/'.join(lineage[:-2])
        else:
            # This should be blog/sub/about
            parent = '/'.join(lineage[:-1])

        return name, parent
