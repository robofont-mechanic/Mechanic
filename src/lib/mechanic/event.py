from mojo.events import postEvent


class Event(object):

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
        parts = [self.subject, tense.capitalize(), self.verb.capitalize()]
        event_name = ''.join(parts)
        postEvent(event_name)
