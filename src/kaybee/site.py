from operator import attrgetter

from kaybee.validators import Validator


class Site:
    def __init__(self, config):
        self.resources = {}
        self.widgets = {}
        self.config = config
        self.validator = Validator()

    @property
    def is_debug(self):
        """ Check the html_theme config to see if we are in debug

         The integration tests run in debug mode which lets templates
         put some markup at the bottom that can be tested E2E.
         """

        return self.config.get('debug', False)

    def add_resource(self, resource):
        """ Add a resource to the db and do any indexing needed """

        self.resources[resource.name] = resource

    def remove_resource(self, name):
        """ Remove a resource from the site and do any unindexing """
        self.resources.pop(name, None)

    def add_widget(self, widget):
        """ Add a widget to the db and do any indexing needed """

        self.widgets[widget.name] = widget

    def remove_widget(self, name):
        """ Remove a widget from the site and do any unindexing """

        self.widgets.pop(name, None)

    def filter_resources(self, rtype=None, sort_value='title',
                         order=1, limit=5, parent_name=None):
        if rtype:
            r1 = [r for r in self.resources.values() if r.rtype == rtype]
        else:
            r1 = self.resources.values()

        # Filter out only those with a parent in their lineage
        if parent_name:
            parent = self.resources[parent_name]
            r2 = [r for r in tuple(r1) if parent in r.parents]
        else:
            r2 = r1

        # Now sorting
        if sort_value:
            if sort_value == 'title':
                # Special case, everything else is in props
                r3 = sorted(
                    r2,
                    key=attrgetter('title')
                )
            else:
                r3 = sorted(
                    r2,
                    key=lambda x: x.props.get(sort_value)
                )
        else:
            r3 = r2

        # Reverse if needed
        if order == -1:
            r3.reverse()

        # Return a limited number
        if limit:
            r3 = r3[:limit]

        return r3

    @property
    def sections(self):
        """ Listing of resources with rtype == section """

        return [s for s in self.resources.values() if s.rtype == 'section']

    @property
    def navmenu(self):
        """ Sorted listing of resources with in_nav set to true """

        resources = [r for r in self.resources.values() if
                     r.props.get('in_nav')]

        # Sort first by title, then by "weight"
        return sorted(resources,
                      key=lambda x: (
                          x.props.get('weight', 0), attrgetter('title')(x))
                      )
