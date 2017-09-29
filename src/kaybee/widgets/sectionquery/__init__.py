from kaybee.core.decorators import kb
from kaybee.widgets import BaseWidget


@kb.widget('sectionquery')
class SectionQuery(BaseWidget):

    def make_context(self, context, site):
        """ Put information into the context for rendering """

        query = self.props['query']
        rtype = query.get('rtype')
        sort_value = query.get('sort_value')
        limit = query.get('limit')
        order = query.get('order')
        parent_name = query.get('parent_name')
        q = dict(rtype=rtype, sort_value=sort_value, limit=limit,
                 order=order, parent_name=parent_name)
        results = site.filter_resources(**q)
        context['result_count'] = len(results)
        context['results'] = results
