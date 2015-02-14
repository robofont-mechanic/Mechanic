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
        logger.info('Calling `{}` in a new thread'.format(target.__name__))
        Thread(target=target,
               args=args,
               kwargs=kwargs).start()
