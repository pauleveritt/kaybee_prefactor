from kaybee.directives.resource import ResourceDirective


def setup(app):
    # Resource directive
    app.add_directive('resource', ResourceDirective)
