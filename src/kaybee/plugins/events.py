"""

Dectate action to manage event callbacks in the configuration.

"""
import dectate


class EventAction(dectate.Action):
    _sphinx_event_names = [
        'env-before-read-docs'
    ]
    config = {
        'events': dict
    }

    def __init__(self, name):
        assert name in self._sphinx_event_names
        super().__init__()
        self.name = name

    def identifier(self, events):
        return self.name

    def perform(self, obj, events):
        events[self.name] = obj

    @classmethod
    def get_callbacks(cls, registry, event_name: str):
        # Presumes the registry has been committed
        q = dectate.Query('event')
        return [args[1] for args in q(registry) if args[0].name == event_name]
