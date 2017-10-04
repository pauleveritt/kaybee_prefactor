import inspect
import os

from docutils.parsers.rst import Directive
from ruamel.yaml import load

from kaybee.core.registry import registry
from kaybee.core.validators import validate


class BaseDirective(Directive):
    has_content = True

    @classmethod
    def get_resource_class(cls, resource_directive):
        """ Make this easy to mock """
        return registry.config.resources[resource_directive]

    @classmethod
    def get_resource_action(cls, kbtype):
        """ Make this easy to mock """
        return registry.first_action('resource', kbtype)

    @property
    def doc_title(self):
        return self.state.parent.parent.children[0].children[0].rawsource

    def validate_resource(self, resource, kbtype):
        props = resource.props
        action_data = self.get_resource_action(kbtype)
        schema_data = action_data.schema
        validate(props, schema_data)

    def run(self):
        """ Run at parse time.

        When the documents are initially being scanned, this method runs
        and does two things: (a) creates an instance that is added to
        the site's widgets, and (b) leaves behind a placeholder docutils
        node that can later be processed after the docs are resolved.
        The latter needs enough information to retrieve the former.

        """

        env = self.state.document.settings.env

        # Get the info from this directive and make instance
        kbtype = self.name
        title = self.doc_title
        resource_content = '\n'.join(self.content)
        resource_class = BaseDirective.get_resource_class(kbtype)
        this_resource = resource_class(env.docname, kbtype,
                                       title, resource_content)
        # If the typedef had an defaults that aren't in the props, add them
        defaults = self.get_resource_action(kbtype).defaults
        if defaults:
            for k, v in defaults.items():
                # TODO 001 Needs tests
                if k not in this_resource.props:
                    this_resource.props[k] = v

        # Validate the properties against the schema for this
        # widget type
        # TODO 001 Get the schema from the registry, not the "site"
        self.validate_resource(this_resource, kbtype)
        site = self.state.document.settings.env.site
        site.add_resource(this_resource)

        # Don't need to return a resource "node", the
        # document is the node
        return []


class BaseResource:
    default_style = ''

    def __init__(self, pagename, rtype, title, content):
        self.name, self.parent = BaseResource.parse_pagename(pagename)
        self.rtype = rtype
        self.title = title
        self.props = BaseResource.load(content)

    @staticmethod
    def load(content):
        """ Provide a way to stub this in tests """

        # If the string of YAML is empty-ish (new lines, etc.)
        # then return an empty dict
        if content.strip() == '':
            return {}
        return load(content)

    @staticmethod
    def parse_pagename(pagename):
        """ Instead of doing this in the constructor, more testable """

        lineage = pagename.split('/')
        lineage_count = len(lineage)

        # Default
        name = pagename
        parent = None

        if lineage_count == 1:
            # This is a doc in the root e.g. index or about
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

    def template(self, site):
        """ Template can come from YAML, section, or class """
        custom_template = self.props.get('template')
        if custom_template:
            return custom_template
        section_doctemplate = self.find_prop(site, 'doc_template')
        if section_doctemplate:
            return section_doctemplate
        return self.__class__.__name__.lower() + '.html'

    def section(self, site):
        """ Which section is this in, if any """

        section = [p for p in self.parents(site) if p.rtype == 'section']
        if section:
            return section[0]
        return None

    def style(self, site):
        """ Get the style from: YAML, hierarchy, or class """

        custom_style = self.find_prop(site, 'style')
        if custom_style:
            return custom_style

        # If the class/instance has style, return it, otherwise none
        return getattr(self, 'default_style', '')

    def parents(self, site):
        """ Split the path in name and get parents """
        if self.name == '/':
            # The root has no parents
            return []
        parents = []
        parent = site.resources.get(self.parent)
        while parent is not None:
            parents.append(parent)
            parent = site.resources.get(parent.parent)
        return parents

    def is_active_section(self, site, nav_href):
        """ Given  href of nav item, determine if resource is in it """

        return self.name.startswith(nav_href)

    def find_prop(self, site, prop_name):
        """ Starting with self, walk until you find prop or None """

        lineage = self.parents(site)
        lineage.insert(0, self)
        for resource in lineage:
            v = resource.props.get(prop_name)
            if v:
                # This resource has the prop, return it
                return v
        return None

    @property
    def navmenu_href(self):
        """ Add .html if needed for links in navmenu """

        # Sections don't need the .html as you point to the container.
        # But if you put a leaf (e.g. an article) in the nav menu,
        # its template needs the href with .html on the end. By default,
        # assume container. Leaf types will override this.

        return self.name

    @classmethod
    def get_schema(cls):
        """ Subclasses or instances can override this """
        class_name = cls.__name__.lower()
        class_filename = inspect.getfile(cls)
        package_dir = os.path.dirname(class_filename)
        schema_filename = os.path.join(package_dir, class_name + '.yaml')
        with open(schema_filename, 'r') as f:
            schema = load(f)
            return schema


def setup(app):
    # Loop through the registered resources and add a directive
    # for each
    for kbtype in registry.config.resources.keys():
        # TODO 001 Have the registry interact with Sphinx and do this?
        app.add_directive(kbtype, BaseDirective)
