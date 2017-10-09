from typing import List, Tuple

from kaybee.core.registry import registry


@registry.widget('kbtoctree')
class KbToctree:
    template = 'kbtoctree.html'
    entries: List = []
    result_count = 0

    def set_entries(self, entries: List[Tuple[str, str]], titles, resources):
        """ Provide the template the data for the toc entries """
        self.entries = []
        for flag, pagename in entries:
            title = titles[pagename].children[0]
            resource = resources.get(pagename.split('/index')[0], None)
            if resource and not resource.is_published():
                continue
            self.entries.append(dict(
                title=title, href=pagename, resource=resource
            ))

        self.result_count = len(self.entries)

    def render(self, builder, context, site):
        """ Given a Sphinx builder and context with site in it,
         generate HTML """

        context['site'] = site
        context['widget'] = self

        html = builder.templates.render(self.template, context)
        return html
