from kaybee.registry import registry


def register_references(app, env, docnames):
    """ Walk the registry and add sphinx directives """

    site = env.site

    for name, klass in registry.config.resources.items():
        # Name is the value in the decorator and directive, e.g.
        # @registry.resource('category') means name=category
        if getattr(klass, 'is_reference', False):
            site.references[name] = dict()
