from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util import logging

from kaybee.resources.query import Query

logger = logging.getLogger(__name__)


class query(nodes.General, nodes.Element):
    pass


class QueryDirective(Directive):
    has_content = True
    required_arguments = 1

    def run(self):
        site = self.state.document.settings.env.site
        name = self.arguments[0]
        content = '\n'.join(self.content)
        query = Query(name, content)

        # TODO If the config says to validate, validate
        site.validator(query)
        site.add(query)
        return []
