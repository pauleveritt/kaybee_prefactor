from typing import List

from pydantic.main import BaseModel

from kaybee.core.registry import registry
from kaybee.widgets import BaseWidget


class QueryModel(BaseModel):
    label: str
    style: str = None
    kbtype: str = None
    limit: int = 5
    parent_name: str = None
    sort_value: str = None
    order: int = 1


class QueryListModel(BaseModel):
    template: str
    queries: List[QueryModel]


@registry.widget('querylist')
class QueryList(BaseWidget):
    model = QueryListModel

    def make_context(self, context, site):
        """ Put information into the context for rendering """

        # Build up some results to put in the context, for each of the
        # nested queries
        result_sets = []
        for query in self.props.queries:
            result_set = dict(
                label=query.label,
                style=query.style,
            )
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
