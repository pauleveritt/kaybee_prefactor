"""

Dectate action to manage resource information in the configuration.

"""

import dectate


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
