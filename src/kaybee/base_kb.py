"""

Use Dectate to make kaybee decorators for configuration.

We need a simple plugin mechanism, to let resource and widget
definitions come from (a) kaybee, (b) other installed packages,
and (c) people writing a Sphinx site that do simple extensions.
We'll use Dectate for that.

"""
import dectate

from kaybee.core_action import CoreAction
from kaybee.plugins.events import EventAction
from kaybee.resources.action import ResourceAction
from kaybee.widgets.action import WidgetAction


class kb(dectate.App):
    core = dectate.directive(CoreAction)
    event = dectate.directive(EventAction)
    resource = dectate.directive(ResourceAction)
    widget = dectate.directive(WidgetAction)
