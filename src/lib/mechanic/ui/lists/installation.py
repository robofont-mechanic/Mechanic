import webbrowser

from mechanic.extension import Extension
from mechanic.ui.lists.base import BaseList
from mechanic.ui.formatters.description import DescriptionFormatter
from mechanic.ui.cells.circle import CircleCell


class InstallationList(BaseList):
    """Return an ExtensionList for installation window."""

    columns = [{"title": "Installed",
                "key": "is_installed",
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

        search = []
        if name:
            search.append(name.lower())
        if extension[u'author']:
            search.append(extension[u'author'].lower())
        if extension[u'description']:
            search.append(extension[u'description'].lower())

        item = {'is_installed': Extension(name=name).is_installed,
                'extension': extension,
                'search': ' '.join(search)}
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
        items = self.getNSTableView().dataSource().selectedObjects()
        if not self._itemsWereDict:
            items = [item["item"] for item in items]
        return self._unwrapListItems(items)
