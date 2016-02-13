import pickle
from lib.tools.notifications import SelectorWrapper


class EventCaller(object):

    def __init__(self, event, callee):
        self.callee = callee
        self.callback = SelectorWrapper(self.call_callee)
        Bus().on(event, self.callback)

    def call_callee(self, notification):
        self.callee(pickle.loads(notification.userInfo()))
