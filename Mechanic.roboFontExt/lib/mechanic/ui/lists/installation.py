import webbrowser

from mechanic.extension import Extension
from mechanic.ui.lists.base import BaseList
from mechanic.ui.formatters.description import DescriptionFormatter
from mechanic.ui.cells.circle import CircleCell


class InstallationList(BaseList):
    """Return an ExtensionList for installation window."""

    columns = [{"title": "Installed",
                "key": "installed",
                "width": 25,
                "editable": False,
                "cell": CircleCell.alloc().init()},
               {"title": "Extension",
                "key": "extension",
                "width": 400,
                "editable": False,
                "formatter": DescriptionFormatter.alloc().init()}]

    def __init__(self, posSize, **kwargs):
        kwargs.update({
            'rowHeight': 39.0,
            'showColumnTitles': False,
            'allowsMultipleSelection': True,
            'doubleClickCallback': self.open_repo
        })

        super(InstallationList, self).__init__(posSize, [], **kwargs)

    def _wrapItem(self, extension):
        name = extension[u'filename'].split("/")[-1]
        item = {'installed': Extension(name=name).installed,
                'extension': extension}
        return super(InstallationList, self)._wrapItem(item)

    def _unwrapListItems(self, items=None):
        if items is None:
            items = super(InstallationList, self).get()
        extensions = [d["extension"] for d in items]
        return extensions

    def set(self, items):
        items = sorted(items, key=lambda e: e['name'].lower())
        super(InstallationList, self).set(items)

    def get(self):
        return self._unwrapListItems()

    def refresh(self):
        self.set(self.get())

    def open_repo(self, sender):
        for item in self.selected:
            webbrowser.open('http://github.com/%s' % item['repository'])

    @property
    def selected(self):
        list_ = self.get()
        selections = self.getSelection()
        return [list_[s] for s in selections]
