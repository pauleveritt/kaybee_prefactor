from sphinx.application import Sphinx
from docutils import nodes

from kaybee import kb
from kaybee.resources.base import BaseResourceModel, BaseResource


class BaseReferenceModel(BaseResourceModel):
    label: str


class BaseReference(BaseResource):
    model = BaseReferenceModel
    is_reference = True


@kb.event('env-before-read-docs', 'references')
def register_references(kb, app, env, docnames):
    """ Walk the registry and add sphinx directives """

    site = env.site

    for name, klass in kb.config.resources.items():
        # Name is the value in the decorator and directive, e.g.
        # @kb.resource('category') means name=category
        if getattr(klass, 'is_reference', False):
            site.references[name] = dict()


@kb.event('env-check-consistency', 'references')
def validate_references(kb: kb, builder, env):
    site = env.site
    for resource in site.resources.values():
        for field_name in resource.reference_fieldnames:
            for target_label in getattr(resource.props, field_name):
                # Make sure this label exists in site.reference
                try:
                    srfn = site.references[field_name]
                except KeyError:
                    msg = f'''\
    Document {resource.name} has unregistered reference "{field_name}"'''
                    raise KeyError(msg)
                try:
                    assert srfn[target_label].props.label == target_label
                except AssertionError:
                    msg = f'''\
    Document {resource.name} has "{field_name}" with orphan {target_label} '''
                    raise KeyError(msg)


@kb.event('missing-reference', 'references')
def missing_reference(app, env, node, contnode):
    site = env.site
    refdoc = node['refdoc']
    target_kbtype, target_label = node['reftarget'].split('-')
    target = site.get_reference(target_kbtype, target_label)

    if node['refexplicit']:
        # The ref has a title e.g. :ref:`Some Title <category-python>`
        dispname = contnode.children[0]
    else:
        # Use the title from the target
        dispname = target.title
    uri = app.builder.get_relative_uri(refdoc, target.name)
    newnode = nodes.reference('', '', internal=True, refuri=uri,
                              reftitle=dispname)

    emp = nodes.emphasis()
    newnode.append(emp)
    emp.append(nodes.Text(dispname))
    return newnode
