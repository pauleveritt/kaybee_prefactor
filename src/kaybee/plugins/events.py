"""

Dectate action to manage event callbacks in the configuration.

"""
import dectate


class EventAction(dectate.Action):
    _sphinx_event_names = [
        'builder-init',
        'env-purge-doc',
        'env-before-read-docs',
        'doctree-read',
        'doctree-resolved',
        'missing-reference',
        'html-collect-pages',
        'env-check-consistency',
        'html-context'
    ]
    config = {
        'events': dict
    }

    def __init__(self, name, scope):
        assert name in self._sphinx_event_names
        super().__init__()
        self.name = name
        self.scope = scope

    def identifier(self, events):
        return self.name + '-' + self.scope

    def perform(self, obj, events):
        events[self.name] = obj

    @classmethod
    def get_callbacks(cls, registry, event_name: str):
        # Presumes the registry has been committed
        q = dectate.Query('event')
        return [args[1] for args in q(registry) if args[0].name == event_name]
