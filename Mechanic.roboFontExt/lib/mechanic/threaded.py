from threading import Thread

from mechanic import logger


class Threaded(object):

    def __init__(self, subject):
        self.subject = subject

    def __call__(self):
        Threaded.run(self.subject)

    def __getattr__(self, attr):
        def wrapped(*args, **kwargs):
            Threaded.run(getattr(self.subject, attr), *args, **kwargs)
        return wrapped

    @staticmethod
    def run(target, *args, **kwargs):
        Threaded.log(target)
        Thread(target=target,
               args=args,
               kwargs=kwargs).start()

    @staticmethod
    def log(target):
        if hasattr(target, 'im_class'):
            logger.info('Calling `%s#%s` in a new thread',
                        target.im_class.__name__,
                        target.__name__)
        else:
            logger.info('Initializing `%s` in a new thread', target.__name__)

class ThreadedObject(object):

    @classmethod
    def initialize_in_thread(cls, *args, **kwargs):
        return Threaded(cls)()

    @property
    def in_thread(self):
        return Threaded(self)
