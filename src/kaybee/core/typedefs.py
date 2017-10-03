""" Extract typedef info from YAML and register
 """
import inspect
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


class KbTypedefInvalidDefault(Exception):
    def __init__(self, default_key):
        f = f'default "{default_key}" does not exist in schema'
        Exception.__init__(self, f)


class KbTypedefReference(Exception):
    def __init__(self, reference):
        f = f'reference "{reference}" does not exist in schema'
        Exception.__init__(self, f)


class YamlTypedef:

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

        # Now ensure that the keys in defaults and values in references,
        # point to things actually in the schema.
        for k in self.defaults.keys():
            if k not in self.schema:
                raise KbTypedefInvalidDefault(k)
        for r in self.references:
            if r not in self.schema:
                raise KbTypedefReference(r)

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
