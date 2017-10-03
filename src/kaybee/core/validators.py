"""
Manage a cache of schemas and validators, then do validation
"""
import inspect
import os

from pykwalify.core import Core


def validate(props, schema_data):
    c = Core(source_data=props, schema_data=schema_data)
    c.validate(raise_exception=True)
