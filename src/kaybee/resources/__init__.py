from kaybee.resources.events import doctree_read_resources


def setup(app):
    app.connect('doctree-read', doctree_read_resources)
