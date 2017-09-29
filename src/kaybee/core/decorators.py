"""
Use Dectate to make kaybee decorators for configuration.

We need a simple plugin mechanism, to let resource and widget
definitions come from (a) kaybee, (b) other installed packages,
and (c) people writing a Sphinx site that do simple extensions.
We'll use Dectate for that.

This registration system provides the following services:

- Register a type of widget/resource for Sphinx node/directive

- Add a template path

- Register the class that will be injected

- Register the schema used to validate the YAML
"""

import dectate


class SiteAction(dectate.Action):
    config = {
        'site': dict
    }

    def __init__(self, name='singleton'):
        super().__init__()
        self.name = name

    def identifier(self, site):
        return self.name

    def perform(self, obj, site):
        site[self.name] = obj


class ResourceAction(dectate.Action):
    config = {
        'resources': dict
    }

    def __init__(self, name):
        super().__init__()
        self.name = name

    def identifier(self, resources):
        return self.name

    def perform(self, obj, resources):
        resources[self.name] = obj
        # Tell the class the name from the decorator
        obj.set_rtype(self.name)


class WidgetAction(dectate.Action):
    config = {
        'widgets': dict
    }

    def __init__(self, name):
        super().__init__()
        self.name = name

    def identifier(self, widgets):
        return self.name

    def perform(self, obj, widgets):
        widgets[self.name] = obj
        # Tell the class the name from the decorator
        obj.set_wtype(self.name)


class kb(dectate.App):
    widget = dectate.directive(WidgetAction)
    resource = dectate.directive(ResourceAction)
    site = dectate.directive(SiteAction)

    @classmethod
    def get_site(cls):
        """ Don't have a way to register a singleton for Dectate """
        query = dectate.Query('site')
        results = list(query(kb))
        return results[0][1]
