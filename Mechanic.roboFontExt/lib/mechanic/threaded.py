from AppKit import NSObject, NSThread

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
        TaskRunner(target=target,
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


class TaskRunner(object):

    separator = "*" * 30

    def __init__(self, target=None, args=None, kwargs=None):
        self.target = target
        self.args = args
        self.kwargs = kwargs
        self.thread = NSThread.alloc().initWithTarget_selector_object_(self, "run:", None)

    def start(self):
        self.thread.start()

    def run_(self, sender):
        try:
            self.target(*self.args, **self.kwargs)
        except:
            import traceback
            errorMessage = [self.separator,
                            traceback.format_exc(5),
                            self.separator]
            print "\n".join(errorMessage)
