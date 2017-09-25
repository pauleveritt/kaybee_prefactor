from kaybee.decorators import kb
from kaybee.widgets import BaseWidget


@kb.widget('sectionquery')
class SectionQuery(BaseWidget):

    def make_context(self, context, site):
        """ Put information into the context for rendering """

        rtype = self.props.get('rtype')
        sort_value = self.props.get('sort_value')
        limit = self.props.get('limit')
        order = self.props.get('order')
        q = dict(rtype=rtype, sort_value=sort_value, limit=limit,
                 order=order)
        results = site.filter_resources(**q)
        context['result_count'] = len(results)
        context['results'] = results
