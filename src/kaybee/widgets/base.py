import inspect
import os
from collections import Mapping

from pydantic import BaseModel
from ruamel.yaml import load

from kaybee.base_types import CoreType


class BaseWidgetModel(BaseModel):
    template: str


class BaseWidget(CoreType):
    kind = 'widget'

    @property
    def template(self):
        """ Allow the template used to come from different places """

        # For now, it comes from a mandatory item in the YAML
        return self.props.template

    def make_context(self, context: Mapping, site):
        pass

    def render(self, builder, context, site):
        """ Given a Sphinx builder and context with site in it,
         generate HTML """

        context['site'] = site
        context['widget'] = self

        # make_context is optionally implemented on the concrete class
        # for each widget
        self.make_context(context, site)

        # NOTE: Can use builder.templates.render_string
        html = builder.templates.render(self.template, context)
        return html

    @classmethod
    def get_schema(cls):
        """ Subclasses or instances can override this """
        class_name = cls.__name__.lower()
        class_filename = inspect.getfile(cls)
        package_dir = os.path.dirname(class_filename)
        schema_filename = os.path.join(package_dir, class_name + '.yaml')
        with open(schema_filename, 'r') as f:
            schema = load(f)
            return schema
