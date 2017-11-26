"""

Dectate action to manage core information in the configuration.

"""
import dectate


class CoreAction(dectate.Action):
    config = {
        'cores': dict
    }

    def __init__(self, name):
        super().__init__()
        self.name = name

    def identifier(self, cores):
        return self.name

    def perform(self, obj, cores):
        cores[self.name] = obj
