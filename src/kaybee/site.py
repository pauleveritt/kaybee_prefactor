from collections import UserDict
from operator import attrgetter, itemgetter

from kaybee.resources.article import Article
from kaybee.resources.homepage import Homepage
from kaybee.resources.section import Section


class Site(UserDict):
    # TODO Make this pluggable, so that outside packages can add
    # to it, perhaps via conf.py.

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.klasses = dict(
            article=Article,
            section=Section,
            homepage=Homepage
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
    def all_resources(self):
        return self.data.values()

    @property
    def sections(self):
        """ Listing of resources with rtype == section """

        return [s for s in self.data.values() if s.rtype == 'section']

    @property
    def navmenu(self):
        """ Sorted listing of resources with rtype == section """

        resources = [r for r in self.data.values() if r.props.get('in_nav')]

        # Sort first by title, then by "weight"
        return sorted(resources,
                      key=lambda x: (
                          x.props['weight'], attrgetter('title')(x))
                      )
