from pydantic.main import BaseModel
from ruamel.yaml import load


class CoreType:
    model: BaseModel

    def __init__(self, pagename: str, kind: str, kbtype: str,
                 title: str, yaml_content: str):
        # Raise custom exception if subclass doesn't have a model attr
        if not getattr(self, 'model'):
            msg = f'Class {self.__class__.__name__} must have model attribute'
            raise AttributeError(msg)

        self.pagename = pagename
        self.kind = kind
        self.kbtype = kbtype
        self.title = title
        self.props = self.load_model(self.model, yaml_content)

    @staticmethod
    def load_model(model, yaml_content: str):
        # If yaml_content is an empty string and parses to None, return
        # empty dic instead
        yaml_props = (load(yaml_content) or {})

        # Make the model, which validates, then do any extra validation
        m = model(**yaml_props)
        return m
