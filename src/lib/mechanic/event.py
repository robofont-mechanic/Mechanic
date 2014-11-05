from mojo.events import postEvent


class evented(object):

    def __init__(self, subject=None, verb=None):
        self.subject = subject
        self.verb = verb

    def __call__(self, fn):
        decorator = self

        def wrapped(self, *args, **kwargs):
            subject = decorator.subject or self.__class__.__name__
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
        return ''.join([
                       self.subject.lower(),
                       tense.capitalize(),
                       self.verb.capitalize()
                       ]


class EventDispatcher(object):

    adapter = RoboFontEvent

    def __init__(self, *args):
        self.event = self.adapter(*args)

    def __enter__(self):
        self.event('will')

    def __exit__(self, error_type, value, trace):
        if error_type is not None:
            self.event('failed')
        else:
            self.event('did')

    def __call__(self, tense):
        self.event(tense)
