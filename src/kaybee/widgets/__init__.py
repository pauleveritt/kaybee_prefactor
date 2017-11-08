from kaybee.widgets.events import process_widget_nodes
from kaybee.widgets.node import widget


def setup(app):
    app.add_node(widget)
    app.connect('doctree-resolved', process_widget_nodes)
