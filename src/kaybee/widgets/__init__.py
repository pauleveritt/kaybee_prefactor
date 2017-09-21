import json
from ruamel.yaml import load


class BaseWidget:
    def __init__(self, content):
        self.content = content
        self.props = self.load(content)

    @staticmethod
    def load(content):
        """ Provide a way to stub this in tests """

        # If the string of YAML is empty-ish (new lines, etc.)
        # then return an empty dict
        if content.strip() == '':
            return {}
        return load(content)

    @property
    def template(self):
        """ Allow the template used to come from different places """

        # For now, it comes from a mandatory item in the YAML
        return self.props['template']

    @property
    def name(self):
        """ Generate a stable, re-usable identifier

         We need a key to store this instance on the site. We don't
         want to make the author's concoct some unique id to add
         in the YAML in the .rst file. Also, if the same widget is
         used in more than one place, we might want to cache the
         results.

         Generate a key as a string from the JSON representation of the
         sorted properties.
         """

        return json.dumps(self.props, sort_keys=True)

    def render(self, builder, context, site):
        """ Given a Sphinx builder and context with site in it,
         generate HTML """

        context['site'] = site
        props = self.props.copy()
        del props['template']
        context['results'] = site.filter_resources(**props)
        html = builder.templates.render(self.template, context)
        return html
