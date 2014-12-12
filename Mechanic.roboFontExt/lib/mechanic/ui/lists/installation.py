from vanilla import List
from mojo.extensions import ExtensionBundle

from mechanic.ui.formatters.description import DescriptionFormatter
from mechanic.ui.cells.circle import CircleCell


class InstallationList(List):
    """Return an ExtensionList for installation window."""

    def __init__(self, posSize, **kwargs):
        columns = [{"title": "Installed",
                    "key": "installed",
                    "width": 25,
                    "editable": False,
                    "cell": CircleCell.alloc().init()},
                   {"title": "Extension",
                    "key": "extension",
                    "width": 200,
                    "editable": False,
                    "formatter": DescriptionFormatter.alloc().init()}]

        super(InstallationList, self).__init__(posSize,
                                               [],
                                               rowHeight=39.0,
                                               columnDescriptions=columns,
                                               showColumnTitles=False,
                                               allowsMultipleSelection=True,
                                               **kwargs)

    def _wrapItem(self, extension):
        name = extension[u'filename'].split("/")[-1]
        item = {'installed': ExtensionBundle(name=name).bundleExists(),
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

    @property
    def selected(self):
        list_ = self.get()
        selections = self.getSelection()
        return [list_[s] for s in selections]
