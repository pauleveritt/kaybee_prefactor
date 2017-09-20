import inspect
import os
from typing import List

from docutils import nodes
from docutils.parsers.rst import Directive
from pykwalify.core import Core
from ruamel.yaml import load
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.util import logging

logger = logging.getLogger(__name__)


class query(nodes.General, nodes.Element):
    pass


class ResourceQuery:
    """ Model stored in the site with the data for this query """

    def __init__(self, name, content):
        self.name = name
        self.props = self.load(content)

    @staticmethod
    def load(content):
        """ Provide a way to stub this in tests """

        # If the string of YAML is empty-ish (new lines, etc.)
        # then return an empty dict
        if content.strip() == '':
            return {}
        return load(content)

    # Schemas and validation
    @classmethod
    def package_dir(cls):
        f = inspect.getfile(cls)
        return os.path.dirname(f)

    @property
    def schema_filename(self):
        """ This is a policy, lowercase of class name + .yaml """

        schema_name = self.__class__.__name__.lower()
        return os.path.join(self.package_dir(), schema_name)

    @property
    def schema(self):
        schema_fn = self.schema_filename + '.yaml'
        with open(schema_fn) as f:
            return load(f.read())

    @staticmethod
    def validate(props, schema):
        c = Core(source_data=props, schema_data=schema)
        c.validate(raise_exception=True)


class QueryDirective(Directive):
    has_content = True

    def run(self) -> List[query]:
        # Insert a docutils node so that we can later (doctree-resolved)
        # come back and process them
        query_node = query('\n'.join(self.content))
        self.state.nested_parse(self.content, self.content_offset, query_node)

        # Now add this to site.queries instead of site.resources


        return [query_node]

# Callback registered with Sphinx's doctree-resolved event
def process_query_nodes(app: Sphinx, doctree, fromdocname):
    # Setup a template and context
    builder: StandaloneHTMLBuilder = app.builder
    ctx = builder.globalcontext.copy()
    templatename = 'query.html'

    for node in doctree.traverse(query):
        # Get the YAML string, parse/validate it
        content = node.children[0].rawsource
        props = node.load(content)

        # Query the "database" based on props in the YAML
        resources = app.env.site.filter_resources(**props)
        ctx['query_results'] = resources

        # Pass the results into Jinja2
        output = builder.templates.render(templatename, ctx)

        # Replace the rendered node contents with raw HTML
        listing = [nodes.raw('', output, format='html')]
        node.replace_self(listing)
