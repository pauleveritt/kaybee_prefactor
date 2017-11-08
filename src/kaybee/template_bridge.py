"""
Sphinx Template Bridge

Sphinx renders the HTML "body". We'd like to customize that without
writing a complete builder. Instead, we'll override the TemplateBridge
and take the HTML rendered output, then customize it before returning.

We'll do that by allowing the registration of a "processor", for example
an XSLT transform.
"""

from sphinx.jinja2glue import BuiltinTemplateLoader

from kaybee.registry import registry


class KaybeeBridge(BuiltinTemplateLoader):

    def render(self, template, context):
        output = super().render(template, context)

        # If there is a registered postrenderer, apply it
        postrenderer = registry.config.cores.get('postrenderer')
        if postrenderer:
            pr = postrenderer()
            output = pr(output)

        return output
