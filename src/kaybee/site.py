from collections import UserDict
from operator import attrgetter

from kaybee.resources.article import Article
from kaybee.resources.homepage import Homepage
from kaybee.resources.section import Section
from kaybee.validators import Validator
from kaybee.widgets.querylist import QueryList


class Site:
    # TODO Make this pluggable, so that outside packages can add
    # to it, perhaps via conf.py.

    def __init__(self, config):
        self.resources = {}
        self.widgets = {}
        self.config = config
        self.klasses = dict(
            article=Article,
            section=Section,
            homepage=Homepage,
            querylist=QueryList
        )
        self._sections = None
        self.validator = Validator()

    def add_resource(self, resource):
        """ Add a resource to the db and do any indexing needed """

        # Make sure the resource's class has been registered
        klassname = resource.__class__.__name__.lower()
        assert klassname in self.klasses
        self.resources[resource.name] = resource

    def remove_resource(self, name):
        """ Remove a resource from the site and do any unindexing """
        self.resources.pop(name, None)

    def add_widget(self, widget):
        """ Add a widget to the db and do any indexing needed """

        # Make sure the resource's class has been registered
        klassname = widget.__class__.__name__.lower()
        assert klassname in self.klasses
        self.widgets[widget.name] = widget

    def remove_widget(self, name):
        """ Remove a widget from the site and do any unindexing """
        self.widgets.pop(name, None)

    def get_class(self, klass_name):
        return self.klasses[klass_name]

    def filter_resources(self, rtype=None, sort_value='title',
                         order=1, limit=5):
        if rtype:
            r1 = [r for r in self.resources.values() if r.rtype == rtype]
        else:
            r1 = self.resources.values()

        # Now sorting
        if sort_value:
            if sort_value == 'title':
                # Special case, everything else is in props
                r2 = sorted(
                    r1,
                    key=attrgetter('title')
                )
            else:
                r2 = sorted(
                    r1,
                    key=lambda x: x.props.get(sort_value)
                )
        else:
            r2 = r1

        # Reverse if needed
        if order == -1:
            r2.reverse()

        # Return a limited number
        if limit:
            r2 = r2[:limit]

        return r2

    @property
    def sections(self):
        """ Listing of resources with rtype == section """

        return [s for s in self.resources.values() if s.rtype == 'section']

    @property
    def navmenu(self):
        """ Sorted listing of resources with rtype == section """

        resources = [r for r in self.resources.values() if
                     r.props.get('in_nav')]

        # Sort first by title, then by "weight"
        return sorted(resources,
                      key=lambda x: (
                          x.props['weight'], attrgetter('title')(x))
                      )
