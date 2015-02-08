from AppKit import NSView
from vanilla import VanillaBaseObject, Sheet, TextBox, ImageView, \
    Button, Group

from mechanic.ui.font import Font
from mechanic.ui.overlay import Overlay


class BaseTab(VanillaBaseObject):
    ns_view_class = NSView
    disabled_text = "Couldn't connect to the Internet..."
    tab_size = (500, 300)

    def __init__(self, dimensions, parent=None):
        self._setupView(self.ns_view_class, dimensions)
        self.parent = parent
        self.content = Group((20, 20, -20, -20))
        self.overlay = Overlay(self.disabled_text)
        self.setup()

    def setup(self):
        pass

    def activate(self):
        pass

    def deactivate(self):
        pass

    def disable(self):
        self.overlay.show(True)

    def enable(self):
        self.overlay.show(False)

    def start_progress(self, *args, **kwargs):
        return self.parent.startProgress(*args, **kwargs)

    def close_notification_sheet(self, sender):
        self.w.notification.close()

    def show_notification_sheet(self, text, size=(300, 80)):
        self.w.notification = Sheet(size, self.parent.w)
        self.w.notification.text = TextBox((15, 15, -50, -15), text)
        self.w.notification.closeButton = Button((-115, -37, 100, 22),
                                                 'Close',
                                                 callback=self.close_notification_sheet)
        self.w.notification.setDefaultButton(self.parent.w.notification.closeButton)
        self.w.notification.open()

    def show_connection_error_sheet(self):
        self.show_notification_sheet(self.disabled_text)

    def set_default_button(self, button):
        self.w.setDefaultButton(button)

    @property
    def w(self):
        return self.parent.w
