from collections import UserDict
from operator import attrgetter

from kaybee.resources.article import Article
from kaybee.resources.section import Section


class Site(UserDict):
    # TODO Make this pluggable, so that outside packages can add
    # to it, perhaps via conf.py.

    def __init__(self):
        super().__init__()
        self.klasses = dict(
            article=Article,
            section=Section
        )
        self._sections = None

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

    @property
    def sections(self):
        """ Cached, sorted listing of resources with rtype == section """

        if self._sections:
            return self._sections
        sections = [s for s in self.data.values() if s.rtype == 'section']

        # Sort first by title, then by "weight"
        sections.sort(key=attrgetter('weight', 'title'))

        # Assign to "cache" and return
        self._sections = sections
        return self._sections
