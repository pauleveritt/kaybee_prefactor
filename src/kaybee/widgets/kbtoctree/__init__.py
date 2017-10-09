from typing import List, Tuple

from kaybee.core.registry import registry


@registry.widget('kbtoctree')
class KbToctree:
    kind = 'widget'
    template = 'kbtoctree.html'
    entries: List = []

    def set_entries(self, entries: List[Tuple[str, str]], titles):
        self.entries = []
        for flag, pagename in entries:
            title = titles[pagename].children[0]
            self.entries.append(dict(title=title, href=pagename))

    def render(self, builder, context, site):
        """ Given a Sphinx builder and context with site in it,
         generate HTML """

        context['site'] = site
        context['widget'] = self

        html = builder.templates.render(self.template, context)
        return html
