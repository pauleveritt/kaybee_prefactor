import inspect
import os
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Mapping, Any, List

from docutils.parsers.rst import Directive
from ruamel.yaml import load

from kaybee.core.core_type import CoreType, ReferencesType
from kaybee.core.registry import registry


class BaseDirective(Directive):
    has_content = True

    @classmethod
    def get_resource_class(cls, resource_directive):
        """ Make this easy to mock """
        return registry.config.resources[resource_directive]

    @property
    def doc_title(self):
        return self.state.parent.parent.children[0].children[0].rawsource

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

        # Add this to the site, and if it is a reference, index it
        site = self.state.document.settings.env.site
        site.resources[this_resource.name] = this_resource
        if hasattr(this_resource, 'label'):
            # This resource is a reference. Find all of the fields
            # that
            label = this_resource.label
            site.add_reference(kbtype, label, this_resource)

        # Don't need to return a resource "node", the
        # document is the node
        return []


class BaseResource(CoreType):
    kind = 'resource'

    def section(self, site):
        """ Which section is this in, if any """

        section = [p for p in self.parents(site) if p.kbtype == 'section']
        if section:
            return section[0]
        return None

    def get_override(self, site, kbtype, propname):
        """ Find a prop either local, overrides, or from class  """

        # Instance
        custom_prop = getattr(self.props, propname)
        if custom_prop:
            return custom_prop

        # Parents...can't use find_prop as have to keep going on overrides
        for parent in self.parents(site):
            overrides = parent.props.overrides
            if overrides:
                kbtype_override = parent.props.overrides.get(self.kbtype)
                if kbtype_override:
                    prop_override = kbtype_override.get(propname)
                    if prop_override:
                        return prop_override

        # Class name
        return self.__class__.__name__.lower() + '.html'

    def template(self, site):
        """ Get the template from: YAML, hierarchy, or class """

        return self.get_override(site, self.kbtype, 'template')

    def style(self, site):
        """ Get the style from: YAML, hierarchy, or class """

        return self.get_override(site, self.kbtype, 'style')

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
            v = getattr(resource.props, prop_name, None)
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

    def extract_toc(self, toc):
        """ Convert HTML markup for toc into a data structure

         In templates, Sphinx provides a ``toc`` in the ``html_context``
         that templates can use to insert an unordered listing of the
         local headings, with internal links. But it's HTML. We want
         to render the markup ourselves. Extract the data from the markup.
         """

        ul = ET.fromstring(toc)
        return [(a.get('href'), a.text) for a in ul.iter('a')]

    def is_published(self):
        """ Return true if this resource has published date in the past """

        now = datetime.now()
        published = self.props.published
        if published:
            return published < now
        return False

    @property
    def reference_fieldnames(self):
        """ Look in model and return each fieldname that is a reference """

        return [
            field.name
            for field in self.props.fields.values()
            if field.type_ == ReferencesType
        ]

    def references(self, site) -> Mapping[str, List[Any]]:
        """ Resolve and return references

         Fields in self.props can flag that they are references by
         using the references type. This method scans the model,
         finds any fields that are references, and returns the
         resources pointed to by those references.

         Note that we shouldn't get to the point of dangling references.
         Our custom Sphinx event should raise a references error
         during the build process (though maybe it is just a warning?)

         """

        references = dict()
        for field in self.props.fields.values():
            if field.type_ != ReferencesType:
                continue

            field_name = field.name
            references[field_name] = []

            # Iterate over each value on this field, e.g.
            # tags: tag1, tag2, tag3
            for target_label in getattr(self.props, field_name):
                # Ask the site to get the object
                target = site.get_reference(field_name, target_label)
                references[field_name].append(target)

        return references


def setup(app):
    # Loop through the registered resources and add a directive
    # for each
    for kbtype in registry.config.resources.keys():
        app.add_directive(kbtype, BaseDirective)
