import pickle

from AppKit import NSDistributedNotificationCenter, NSThread
from lib.tools.notifications import SelectorWrapper


class Bus(object):

    def on(self, event, observer):
        self.dispatch.addObserver_selector_name_object_(observer, "action:", Bus.namespace(event), None)

    def emit(self, event, data):
        self.dispatch.postNotificationName_object_userInfo_(Bus.namespace(event), None, pickle.dumps(data))

    @property
    def dispatch(self):
        return NSDistributedNotificationCenter.defaultCenter()

    @staticmethod
    def namespace(event):
        return "mechanic.{}".format(event)
