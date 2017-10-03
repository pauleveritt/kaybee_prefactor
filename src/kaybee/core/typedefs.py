""" Extract typedef info from YAML and register
 """
import inspect
from typing import Dict, Sequence

import os

from pykwalify.core import Core
from ruamel.yaml import load_all

import kaybee

typeinfo_path = os.path.join(
    os.path.dirname(inspect.getfile(kaybee)),
    'core/typeinfo.yaml'
)


class KbTypedefDocsError(Exception):
    def __init__(self):
        Exception.__init__(self, 'typedef files need two YAML documents')


class YamlTypedef:
    kind: str
    kbtype: str
    defaults: Dict
    references: Sequence
    schema: Dict

    def read(self):
        with open(self.yaml_fn) as f:
            self.yaml_content = f.read()

    def load(self):
        docs = list(load_all(self.yaml_content))
        if len(docs) != 2:
            raise KbTypedefDocsError()
        self.typeinfo, self.schema = docs

    def validate(self):
        c = Core(source_data=self.typeinfo, schema_files=[typeinfo_path])
        c.validate(raise_exception=True)

    def __init__(self, yaml_fn=None):
        self.yaml_fn = yaml_fn
        self.yaml_content = None
        self.typeinfo = None
        self.schema = None

        # Now do each phase of processing
        self.read()
        self.load()
        self.validate()

    @property
    def kind(self):
        return self.typeinfo['kind']

    @property
    def kbtype(self):
        return self.typeinfo['kbtype']

    @property
    def defaults(self):
        return self.typeinfo.get('defaults', dict())

    @property
    def references(self):
        return self.typeinfo.get('references', [])

    @property
    def klass(self):
        return self.typeinfo['kind']
