import inspect
import os
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Mapping, Any, List

from pydantic import BaseModel
from ruamel.yaml import load

from kaybee.base_types import CoreType, ReferencesType


class BaseResourceModel(BaseModel):
    """ Kaybee default schema definitions for resources """

    template: str = None
    style: str = None
    in_nav: bool = False
    weight: int = 0
    published: datetime = None
    category: ReferencesType = []
    tag: ReferencesType = []
    excerpt: str = None
    auto_excerpt: int = 1


class BaseContainerModel(BaseResourceModel):
    """ A resource that is a parent for other resources

     Parents can override child properties based on kbtype

    E.g.

    overrides:
        article:
            template: customtemplate.html
            style: boldestbaddest

     """
    overrides: Mapping[str, Mapping[str, str]] = None


class BaseResource(CoreType):
    kind = 'resource'
    toctree = []
    title = None
    excerpt = None

    def section(self, site):
        """ Which section is this in, if any """

        section = [p for p in self.parents(site) if p.kbtype == 'section']
        if section:
            return section[0]
        return None

    def find_prop(self, site, prop_name):
        """ Starting with self, walk until you find prop or None """

        # Instance
        custom_prop = getattr(self.props, prop_name, None)
        if custom_prop:
            return custom_prop

        # Parents...can't use find_prop as have to keep going on overrides
        for parent in self.parents(site):
            overrides = parent.props.overrides
            if overrides:
                # First try in the per-type overrides
                kbtype_overrides = overrides.get(self.kbtype)
                if kbtype_overrides:
                    prop_override = kbtype_overrides.get(prop_name)
                    if prop_override:
                        return prop_override

                # Next in the "all" section of overrides
                all_overrides = overrides.get('all')
                if all_overrides:
                    prop_override = all_overrides.get(prop_name)
                    if prop_override:
                        return prop_override

        return

    def template(self, site):
        """ Get the template from: YAML, hierarchy, or class """

        template_name = self.find_prop(site, 'template')
        if template_name:
            return template_name
        else:
            return self.__class__.__name__.lower() + '.html'

    def style(self, site):
        """ Get the style from: YAML or hierarchy """

        return self.find_prop(site, 'style')

    def parents(self, site):
        """ Split the path in name and get parents """

        if self.docname == 'index':
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

        # The navhref might end with '/index' so remove it if so
        if nav_href.endswith('/index'):
            nav_href = nav_href[:-6]

        return self.name.startswith(nav_href)

    @property
    def navmenu_href(self):
        """ Add .html if needed for links in navmenu """

        return self.name + '.html'

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

    def series(self, site):
        parent = site.resources.get(self.parent)
        if not parent:
            return None
        results = []
        for docname in parent.toctree:
            resource = site.resources.get(docname)
            if resource:
                # We might have a non-resource page in the toctree,
                # so skip it if true
                excerpt = getattr(resource.excerpt, 'excerpt', False)
                results.append(
                    dict(
                        docname=docname,
                        title=resource.title,
                        excerpt=resource.excerpt,
                        current=self.docname == docname
                    )
                )
        return results

    def to_json(self, site):
        d = super().to_json(site)
        d['template'] = self.template(site)
        d['title'] = self.title
        d['excerpt'] = self.excerpt
        d['style'] = self.style(site)
        d['section'] = getattr(self.section(site), 'name', '')
        d['in_nav'] = self.props.in_nav
        d['weight'] = self.props.weight
        d['toctree'] = self.toctree
        d['published'] = self.props.published
        d['references'] = [r.docname for r in
                           self.references(site)['category']]
        try:
            d['series'] = self.series(site)
        except AttributeError:
            d['series'] = []
        return d
