"""
Manage a cache of schemas and validators, then do validation
"""
import inspect
import os

from pykwalify.core import Core


class Validators:
    @classmethod
    def validate(cls, resource):
        """ Given a resource with props, validate it against the schema
         name registered on this class """

        props = resource.props
        class_name = resource.__class__.__name__.lower()

        # Ask the resource for its schema filename
        schema_filename = getattr(resource, 'schema_filename', None)
        if schema_filename is None:
            # Adopt a site policy of looking for the schema as a
            # resourectype.yaml filename (e.g. article.yaml) in the
            # same directory as the class.
            class_filename = inspect.getfile(resource.__class__)
            package_dir = os.path.dirname(class_filename)
            schema_filename = os.path.join(package_dir, class_name + '.yaml')

        c = Core(source_data=props, schema_files=[schema_filename])
        c.validate(raise_exception=True)
