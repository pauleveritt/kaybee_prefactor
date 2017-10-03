"""

Use Dectate to make kaybee decorators for configuration.

We need a simple plugin mechanism, to let resource and widget
definitions come from (a) kaybee, (b) other installed packages,
and (c) people writing a Sphinx site that do simple extensions.
We'll use Dectate for that.

This registration system provides the following services:

- Register a type of widget/resource for Sphinx node/directive

- Register the class that will be injected

- Register the schema used to validate the YAML

"""
import dectate


class KbActionInvalidKind(Exception):
    def __init__(self, kind):
        fmt = f'registry has no class attribute action "{kind}"'
        Exception.__init__(self, fmt)


class SiteAction(dectate.Action):
    config = {
        'site': dict
    }

    def __init__(self):
        super().__init__()
        self.name = 'singleton'

    def identifier(self, site):
        return self.name

    def perform(self, obj, site):
        site[self.name] = obj


class ResourceAction(dectate.Action):
    config = {
        'resources': dict
    }

    def __init__(self, name, defaults=None, references=None):
        super().__init__()
        self.name = name
        self.defaults = defaults
        self.references = references

    def identifier(self, resources):
        return self.name

    def perform(self, obj, resources):
        resources[self.name] = obj


class WidgetAction(dectate.Action):
    config = {
        'widgets': dict
    }

    def __init__(self, name, defaults=None, references=None):
        super().__init__()
        self.name = name
        self.defaults = defaults
        self.references = references

    def identifier(self, widgets):
        return self.name

    def perform(self, obj, widgets):
        widgets[self.name] = obj


class registry(dectate.App):
    widget = dectate.directive(WidgetAction)
    resource = dectate.directive(ResourceAction)
    site = dectate.directive(SiteAction)

    @classmethod
    def add_action(cls, kind, kbtype, klass, defaults=None,
                   references=None):
        """ YAML types imperatively add config per contract """

        # Get the kind, raise custom exception if it doesn't exist
        k = getattr(cls, kind, None)
        if k is None:
            raise KbActionInvalidKind(kind)

        k(kbtype, defaults=defaults, references=references)(klass)

    @classmethod
    def first_action(cls, kind, kbtype):
        """ Get type config info from the kbtype of certain kind """
        qr = dectate.Query(kind)
        # Use a generator expression to get the first action
        # in "kind" with a name of ktype. kind might be
        # "resource" or "widget", kbtype might be "article".
        return next((x for x in qr.filter(name=kbtype)(cls)))[0]

    @classmethod
    def get_class(cls, kind, kbtype):
        q = dectate.Query(kind)
        klass = [i[1] for i in list(q(cls)) if i[0].name == kbtype][0]
        return klass

    @classmethod
    def get_site(cls, sitename='site'):
        """ Don't have a way to register a singleton for Dectate """
        query = dectate.Query(sitename)
        results = list(query(cls))
        return results[0][1]
