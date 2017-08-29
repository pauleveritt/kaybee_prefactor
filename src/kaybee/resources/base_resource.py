import inspect
import os

from pykwalify.core import Core
from ruamel.yaml import load


class BaseResource:
    def __init__(self, pagename, rtype, title, content):
        self.name, self.parent = BaseResource.parse_pagename(pagename)
        # if pagename[-6:] == '/index':
        #     # Remove /index from the resource name
        #     self.name = pagename[:-6]
        #     self.parent = '/'.join(self.name.split('/')[:-1])
        # elif pagename == 'index':
        #     # This is the root of the doctree
        #     self.name = '/'
        #     self.parent = None
        # else:
        #     self.name = pagename
        #     self.parent = '/'.join(self.name.split('/')[:-1])
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
            parent = lineage[-3]
        else:
            # This should be blog/sub/about
            parent = lineage[-2]

        return name, parent
