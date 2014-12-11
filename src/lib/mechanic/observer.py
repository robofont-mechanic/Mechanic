from mojo.events import addObserver


class Observer(object):

    def add(self, method, *events):
        for event in events:
            addObserver(self, method, event)

    def remove(self, *events):
        for event in events:
            removeObserver(self, event)
