from AppKit import NSDistributedNotificationCenter, NSThread
from lib.tools.notifications import SelectorWrapper


class Bus(object):

    def on(self, event, action):
        namespacedEvent = "mechanic.{}".format(event)
        wrapped = SelectorWrapper(action)

        self.dispatch.addObserver_selector_name_object_(wrapped, "action:", namespacedEvent, None)

    def emit(self, event, data):
        self.dispatch.postNotificationName_object_userInfo_(event, None, data)

    @property
    def dispatch(self):
        return NSDistributedNotificationCenter.defaultCenter()
