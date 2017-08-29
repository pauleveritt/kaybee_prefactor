import inspect
import os

from pykwalify.core import Core
from ruamel.yaml import load


class BaseResource:
    def __init__(self, pagename, rtype, title, content):
        self.name, self.parent = BaseResource.parse_pagename(pagename)
        self.rtype = rtype
        self.title = title
        self.props = BaseResource.load(content)

    @staticmethod
    def load(content):
        """ Provide a way to stub this in tests """
        return load(content)

    @staticmethod
    def parse_pagename(pagename):
        """ Instead of doing this in the constructor, more testable """

        lineage = pagename.split('/')
        lineage_count = len(lineage)

        # Default
        name = pagename
        parent = None

        if pagename == 'index':
            # This is the root of the doctree
            name = '/'
        elif lineage_count == 1:
            # This is a doc in the root e.g. about
            parent = '/'
        elif lineage_count == 2 and lineage[-1] == 'index':
            # This is blog/index, parent is the root
            name = lineage[0]
            parent = '/'
        elif lineage_count == 2:
            # This is blog/about
            parent = lineage[0]
        elif lineage[-1] == 'index':
            # This is blog/sub/index
            name = '/'.join(lineage[:-1])
            parent = '/'.join(lineage[:-2])
        else:
            # This should be blog/sub/about
            parent = '/'.join(lineage[:-1])

        return name, parent

    @classmethod
    def package_dir(cls):
        f = inspect.getfile(cls)
        return os.path.dirname(f)

    @property  # TODO Re-ify this in some way
    def template(self):
        return self.__class__.__name__.lower()

    def parents(self, site):
        """ Split the path in name and get parents """
        if self.name == '/':
            # The root has no parents
            return []
        parents = []
        parent = site.get(self.parent)
        while parent is not None:
            parents.append(parent)
            parent = site.get(parent.parent)
        return parents

    def findProp(self, site, prop_name):
        """ Starting with self, walk until you find prop or None """

        lineage = self.parents(site)
        lineage.insert(0, self)
        for resource in lineage:
            v = resource.props.get(prop_name)
            if v:
                # This resource has the prop, return it
                return v
        return None
