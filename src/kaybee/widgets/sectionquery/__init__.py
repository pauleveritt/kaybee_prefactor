from pydantic import BaseModel

from kaybee.core.registry import registry
from kaybee.widgets import BaseWidget


class QueryModel(BaseModel):
    kbtype: str = None
    limit: int = 5
    parent_name: str = None
    sort_value: str = None
    order: int = 1


class SectionQueryModel(BaseModel):
    template: str
    query: QueryModel


@registry.widget('sectionquery')
class SectionQuery(BaseWidget):
    model = SectionQueryModel

    def make_context(self, context, site):
        """ Put information into the context for rendering """

        query = self.props.query
        kbtype = query.kbtype
        sort_value = query.sort_value
        limit = query.limit
        order = query.order
        parent_name = query.parent_name
        q = dict(kbtype=kbtype, sort_value=sort_value, limit=limit,
                 order=order, parent_name=parent_name)
        results = site.filter_resources(**q)
        context['result_count'] = len(results)
        context['results'] = results
