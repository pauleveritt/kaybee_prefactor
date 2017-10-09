from sphinx.addnodes import toctree

from kaybee.core.registry import registry


@registry.widget('kbtoctree')
class KbToctree:
    kind = 'widget'
    template = 'kbtoctree.html'

    def render(self, builder, context, site, node: toctree, titles):
        """ Given a Sphinx builder and context with site in it,
         generate HTML """

        context['site'] = site
        context['widget'] = self

        _entries = []
        for entry in node.attributes['entries']:
            pagename = entry[1]
            title = titles[pagename].children[0]
            href = pagename
            _entries.append(dict(title=title, href=href))
        context['entries'] = _entries

        html = builder.templates.render(self.template, context)
        return html
