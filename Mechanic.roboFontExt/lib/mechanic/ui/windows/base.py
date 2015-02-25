from vanilla import Window, Tabs
from defconAppKit.windows.baseWindow import BaseWindowController

from mechanic.lazy_property import lazy_property
from mechanic.ui.toolbar import Toolbar


class BaseWindow(BaseWindowController):
    window_size = (500, 300)

    def open(self, active="Install"):
        if self.toolbar.items:
            self.create_toolbar()
            self.add_tabs()
            self.set_active_tab(active)
        self.w.open()
        return self

    def create_toolbar(self):
        self.w.addToolbar(toolbarIdentifier="mechanicToolbar",
                          toolbarItems=self.toolbar.items,
                          addStandardItems=False)

    def set_active_tab(self, pane):
        current_index = self.w.tabs.get()
        index = self.toolbar.index_of(pane)
        if not self.w.isVisible():
            self.w.getNSWindow().toolbar().setSelectedItemIdentifier_(pane)
        self.w.tabs.set(index)
        self.w.tabs[current_index].view.deactivate()
        self.set_window_size(self.w.tabs[index].view)
        self.w.tabs[index].view.activate()

    def toolbar_select(self, sender):
        self.set_active_tab(sender.itemIdentifier())

    def add_tabs(self):
        self.w.tabs = Tabs((0, 0, -0, -0), self.toolbar.labels, showTabs=False)

        for index, item in enumerate(self.toolbar.items):
            tab = self.w.tabs[index]
            tab.view = item['view']((0, 0, -0, -0), self)

    def set_window_size(self, tab):
        self.w.resize(tab.tab_size[0], tab.tab_size[1], False)

    def start_progress(self, *args, **kwargs):
        return self.startProgress(*args, **kwargs)

    @property
    def current_tab(self):
        index = self.w.tabs.get()
        return self.w.tabs[index]

    @lazy_property
    def toolbar(self):
        return Toolbar(self)

    @lazy_property
    def w(self):
        return Window(self.window_size,
                      autosaveName=self.__class__.__name__,
                      title=self.window_title)

