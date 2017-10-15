from typing import List

from pydantic.main import BaseModel

from kaybee.core.core_type import CoreQueryModel
from kaybee.core.registry import registry
from kaybee.widgets.base import BaseWidget


class QuerySectionModel(BaseModel):
    label: str
    style: str = None
    query: CoreQueryModel


class QueryListModel(BaseModel):
    template: str
    queries: List[QuerySectionModel]


@registry.widget('querylist')
class QueryList(BaseWidget):
    model = QueryListModel

    def make_context(self, context, site):
        """ Put information into the context for rendering """

        # Build up some results to put in the context, for each of the
        # nested queries
        result_sets = []
        for query_section in self.props.queries:
            result_set = dict(
                label=query_section.label,
                style=query_section.style,
            )
            query = query_section.query
            kbtype = query.kbtype
            sort_value = query.sort_value
            limit = query.limit
            order = query.order
            q = dict(kbtype=kbtype, sort_value=sort_value, limit=limit,
                     order=order)
            results = site.filter_resources(**q)
            result_set['results'] = results
            result_sets.append(result_set)

        context['result_sets'] = result_sets
