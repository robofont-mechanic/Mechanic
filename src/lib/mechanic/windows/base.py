from vanilla import Window, Tabs
from defconAppKit.windows.baseWindow import BaseWindowController
from mojo.events import addObserver


class BaseWindow(BaseWindowController):

    def __init__(self, active="Install"):
        self.first_tab = active
        self.w = Window((500,300),
                        autosaveName=self.__class__.__name__,
                        title=self.window_title)

        self.watch("repositoryWillRead")#, 'Getting %s...' % extension.config.repository
        self.watch("repositoryDidRead")

        self.watch("repositoryWillDownload")#, 'Downloading %s...' % extension.bundle.name
        self.watch("repositoryDidDownloadChunk")
        self.watch("repositoryDidDownload")

        self.watch("repositoryWillExtractDownload")#, 'Extracting %s...' % extension.bundle.name
        self.watch("repositoryDidExtractDownload") #

        self.watch("extensionWillInstall")#, 'Installing %s...' % extension.bundle.name
        self.watch("extensionDidInstall")

        self.__toolbar_items = []

    def watch(self, event_name, message=None):
        addObserver(self, "print_info", event_name)

    def print_info(self, info):
        print info

    def open(self):
        if self.__toolbar_items:
            self.createToolbar()
            self.addTabs()
            self.setActivePane(self.first_tab)
        self.w.open()

    def addToolbarItem(self, **kwargs):
        item = dict(itemIdentifier=kwargs['title'],
                    label=kwargs['title'],
                    callback=self.toolbarSelect,
                    imageNamed=kwargs['image'],
                    selectable=True,
                    view=kwargs['view'])
        self.__toolbar_items.append(item)

    def createToolbar(self):
        self.w.addToolbar(toolbarIdentifier="mechanicToolbar",
                          toolbarItems=self.__toolbar_items,
                          addStandardItems=False)

    def setActivePane(self, pane):
        current_index = self.w.tabs.get()
        index = self.tabIndex(pane)
        if not self.w.isVisible():
            self.w.getNSWindow().toolbar().setSelectedItemIdentifier_(pane)
        self.w.tabs.set(index)
        self.w.tabs[current_index].view.deactivate()
        self.w.tabs[index].view.setWindowSize()
        self.w.tabs[index].view.activate()

    def toolbarSelect(self, sender):
        self.setActivePane(sender.itemIdentifier())

    def addTabs(self):
        self.w.tabs = Tabs((0, 0, -0, -0),
                           [item['label'] for item in self.__toolbar_items],
                           showTabs=False)

        for index, item in enumerate(self.__toolbar_items):
            tab = self.w.tabs[index]
            tab.view = item['view']((0,0,-0,-0), self)

    def tabIndex(self, label):
        return next((index for index, item
                           in enumerate(self.__toolbar_items)
                           if item['label'] == label), 0)
