

def register_references(app, env, docnames):
    """ Walk the registry and add sphinx directives """

    from kaybee import kb

    site = env.site

    for name, klass in kb.config.resources.items():
        # Name is the value in the decorator and directive, e.g.
        # @kb.resource('category') means name=category
        if getattr(klass, 'is_reference', False):
            site.references[name] = dict()
