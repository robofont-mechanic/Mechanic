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

    def watch(self, event_name, message=None):
        addObserver(self, "print_info", event_name)

    def print_info(self, info):
        print info

    def open(self):
        if self.toolbar.items:
            self.createToolbar()
            self.addTabs()
            self.setActivePane(self.first_tab)
        self.w.open()

    def createToolbar(self):
        self.w.addToolbar(toolbarIdentifier="mechanicToolbar",
                          toolbarItems=self.toolbar.items,
                          addStandardItems=False)

    def setActivePane(self, pane):
        current_index = self.w.tabs.get()
        index = self.toolbar.index_of(pane)
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
                           [item['label'] for item in self.toolbar.items],
                           showTabs=False)

        for index, item in enumerate(self.toolbar.items):
            tab = self.w.tabs[index]
            tab.view = item['view']((0,0,-0,-0), self)

    @property
    def toolbar(self):
        try:
            return self.__toolbar
        except AttributeError:
            self.__toolbar = Toolbar(self)
            return self.__toolbar


class Toolbar(object):
    
    def __init__(self, window):
        self.items = []
        self.window = window
    
    def index_of(self, label):
        return next((index for index, item
                           in enumerate(self.items)
                           if item['label'] == label), 0)

    def add_item(self, view):
        item = dict(itemIdentifier=view.title,
                    label=view.title,
                    callback=self.window.toolbarSelect,
                    imageNamed=view.image,
                    selectable=True,
                    view=view)
        self.items.append(item)
