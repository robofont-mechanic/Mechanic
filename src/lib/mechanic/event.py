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


class EventDispatcher(object):

    def __init__(self, object_, subject, verb):
        self.object = object_
        self.subject = subject
        self.verb = verb

    def __enter__(self):
        self.post('will')

    def __exit__(self, error_type, value, trace):
        if error_type is not None:
            self.post('failed')
        else:
            self.post('did')

    def post(self, tense):
        postEvent(self.event_name(tense), **{self.subject: self.object})

    def event_name(self, tense):
        return ''.join(self.event_name_parts(tense))

    def event_name_parts(self, tense):
        return [
               self.subject.lower(),
               tense.capitalize(),
               self.verb.capitalize()
               ]
