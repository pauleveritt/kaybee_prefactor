""" Centralize definition of types

You can register stuff in kaybee in several ways: YAML in the
docs project's conf area, classes in the docs project's conf area,
and of course kaybee's builtin types (article, section, homepage, etc.)

We need to route the discovery and validation through some common
policies.

 """
import inspect
from typing import Dict

import os

from pykwalify.core import Core
from ruamel.yaml import load_all

import kaybee

typeinfo_path = os.path.join(
    os.path.dirname(inspect.getfile(kaybee)),
    'core/typeinfo.yaml'
)


class KbTypedefDocsError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, 'typedef files need two YAML documents')


class KbTypedef:
    kind: str
    name: str
    schema: Dict

    def __init__(self, kind='', name='', yaml_fn=None):
        if yaml_fn:
            with open(yaml_fn, 'r') as f:
                content = f.read()
                docs = list(load_all(content))
                if len(docs) != 2:
                    raise KbTypedefDocsError()
                typeinfo, schema = docs

                # Validate the typedef
                c = Core(source_data=typeinfo, schema_files=[typeinfo_path])
                c.validate(raise_exception=True)

