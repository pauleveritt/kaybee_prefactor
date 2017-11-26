"""

Dectate action to manage widget information in the configuration.

"""

import dectate


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
