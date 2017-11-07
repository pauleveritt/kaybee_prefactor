from kaybee.registry import registry
from kaybee.widgets.directive import BaseWidgetDirective
from kaybee.widgets.events import process_widget_nodes
from kaybee.widgets.node import widget


def setup(app):
    # Loop through the registered widgets and add a directive
    # for each
    app.add_node(widget)
    for kbtype in registry.config.widgets.keys():
        app.add_directive(kbtype, BaseWidgetDirective)

    app.connect('doctree-resolved', process_widget_nodes)
