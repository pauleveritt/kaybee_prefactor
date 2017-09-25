from kaybee.decorators import kb
from kaybee.widgets import BaseWidget


@kb.widget('querylist')
class QueryList(BaseWidget):

    def make_context(self, context, site):
        """ Put information into the context for rendering """

        # Build up some results to put in the context, for each of the
        # nested queries
        result_sets = []
        for query in self.props['queries']:
            result_set = dict(
                label=query.get('label'),
                style=query.get('style'),
            )
            rtype = query.get('rtype')
            sort_value = query.get('sort_value')
            limit = query.get('limit')
            order = query.get('order')
            q = dict(rtype=rtype, sort_value=sort_value, limit=limit,
                     order=order)
            results = site.filter_resources(**q)
            result_set['results'] = results
            result_sets.append(result_set)

        context['result_sets'] = result_sets
