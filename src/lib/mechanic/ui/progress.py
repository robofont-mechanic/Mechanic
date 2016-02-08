from mojo.events import addObserver, removeObserver


class each(object):

    def __init__(self, countable):
        self.countable = countable

    def __call__(self, fn):

        try:
            ticks = fn.ticks
        except:
            ticks = 0

        def wrapped(ui, *args, **kwargs):
            count = len(eval('ui.{}'.format(self.countable)))
            ui.progress = ui.start_progress('', count * ticks)
            fn(ui, *args, **kwargs)
            ui.progress.close()

        return wrapped


class tick(object):

    def __init__(self, event, message=""):
        self.event = event
        self.message = message

    def __call__(self, fn):

        def wrapped(self_, *args, **kwargs):
            self.ui = self_
            with self: fn(self_, *args, **kwargs)

        try:
            wrapped.ticks = fn.ticks + 1
        except:
            wrapped.ticks = 1

        return wrapped

    def __enter__(self):
        self.setup()
        addObserver(self, 'run', self.event)

    def __exit__(self, error, value, trace):
        removeObserver(self, self.event)
        self.teardown()

    def setup(self):
        pass

    def teardown(self):
        pass

    def run(self, sender):
        message = self.formatted_message(**sender)
        self.ui.progress.update(message)

    def formatted_message(self, **spec):
        return u"{}\u2026".format(self.message.format(**spec))
