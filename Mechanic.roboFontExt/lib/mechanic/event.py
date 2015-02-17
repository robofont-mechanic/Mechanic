import re

from mojo.events import postEvent


def to_camelcase(s):
    return re.sub(r'(?!^)_([a-zA-Z])', lambda m: m.group(1).upper(), s)


class evented(object):

    def __init__(self, subject=None, verb=None):
        self.subject = subject
        self.verb = verb

    def __call__(self, fn):
        decorator = self

        def wrapped(self, *args, **kwargs):
            subject = decorator.subject or self.__class__.__name__.lower()
            verb = decorator.verb or fn.__name__

            with EventDispatcher(self, subject, verb):
                return fn(self, *args, **kwargs)

        return wrapped


class RoboFontEvent(object):

    def __init__(self, object_, subject, verb):
        self.object = object_
        self.subject = subject
        self.verb = verb

    def __call__(self, tense):
        postEvent(self.name(tense), **{self.subject: self.object})

    def name(self, tense):
        return to_camelcase('_'.join([self.subject, tense, self.verb]))


class EventDispatcher(object):

    adapter = RoboFontEvent

    def __init__(self, *args):
        self.event = self.adapter(*args)

    def __enter__(self):
        self.event('will')

    def __exit__(self, error, value, trace):
        if error is not None:
            self.event('failed')
        else:
            self.event('did')

    def __call__(self, tense):
        self.event(tense)
