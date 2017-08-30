from collections import UserDict

from kaybee.resources.article import Article


class Site(UserDict):
    # TODO Make this pluggable, so that outside packages can add
    # to it, perhaps via conf.py.

    def __init__(self):
        super().__init__()
        self.klasses = dict(
            article=Article
        )

    def add(self, resource):
        """ Add a resource to the db and do any indexing needed """

        # Make sure the resource's class has been registered
        klassname = resource.__class__.__name__.lower()
        assert klassname in self.klasses
        self[resource.name] = resource

    def remove(self, name):
        """ Remove a resource from the site and do any unindexing """
        self.pop(name, None)

    def get_class(self, klass_name):
        return self.klasses[klass_name]
