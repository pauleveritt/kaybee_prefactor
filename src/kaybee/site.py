from operator import attrgetter


class Site:
    def __init__(self, config):
        self.resources = {}
        self.widgets = {}
        self.genericpages = {}
        self.config = config
        self.references = {}

    @property
    def is_debug(self):
        """ Check the html_theme config to see if we are in debug

         The integration tests run in debug mode which lets templates
         put some markup at the bottom that can be tested E2E.
         """

        return self.config.is_debug

    def filter_resources(self, kbtype=None, sort_value='title',
                         order=1, limit=5, parent_name=None,
                         props=[], is_published=True):

        # Start with (hopefully) most common, filter based on resource type
        if kbtype:
            r1 = [r for r in self.resources.values() if r.kbtype == kbtype]
        else:
            r1 = list(self.resources.values())

        # Filter those results based on arbitrary key-value pairs
        for prop in props:
            r1 = [r for r in r1
                  if getattr(r.props, prop.key, None) == prop.value]

        # Filter out only those with a parent in their lineage
        if parent_name:
            parent = self.resources[parent_name]
            r2 = [r for r in r1 if parent in r.parents(self)]
        else:
            r2 = r1

        # Apply the "is_published" filter, if present
        if is_published:
            r2 = [resource for resource in r2 if resource.is_published()]

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
                    key=lambda x: getattr(x.props, sort_value, 0)
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
        """ Listing of published resources with kbtype == section """

        return [s for s in self.resources.values()
                if s.kbtype == 'section' and s.is_published()]

    def get_reference(self, kbtype: str, label: str):
        """ Return reference filed under kbtype/label

         The references are organized by field/label, e.g. category/cat1.
         This lets us use a shorthand notation to go the resource, e.g.
         ref:category:cat1 instead of folder1/folder2/cat1.
         """

        return self.references[kbtype][label]

    def add_reference(self, kbtype: str, label: str, target):
        """ Add reference object in references under kbtype/label=target """

        # if kbtype not in self.references:
        #     self.references[kbtype] = dict()
        self.references[kbtype][label] = target

    @property
    def navmenu(self):
        """ Sorted listing of published resources with in_nav set to true """

        resources = [r for r in self.resources.values() if
                     r.props.in_nav and r.is_published()]

        # Sort first by title, then by "weight"
        return sorted(resources,
                      key=lambda x: (
                          x.props.weight, attrgetter('title')(x))
                      )
