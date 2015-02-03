from vanilla import CheckBoxListCell

from mechanic.update import Update
from mechanic.storage import Storage
from mechanic.ui.lists.extension import ExtensionList
from mechanic.ui.formatters.version import VersionFormatter


class UpdateList(ExtensionList):
    """Return an ExtensionList for updates window."""

    columns = [{"title": "Install",
                "key": "install",
                "width": 40,
                "editable": True,
                "cell": CheckBoxListCell()},
               {"title": "Extension",
                "key": "name",
                "width": 300,
                "editable": False},
               {"title": "Version",
                "key": "remote_version",
                "width": 60,
                "editable": False,
                "formatter": VersionFormatter.alloc().init()}]

    def __init__(self, posSize, **kwargs):
        super(UpdateList, self).__init__(posSize, [], **kwargs)

    def refresh(self, force=False):
        try:
            self.set(Update.all(force))
        except Update.ConnectionError:
            print "Mechanic: Couldn't connect to the internet"
            return

    def _wrapItem(self, extension):
        item = super(UpdateList, self)._wrapItem(extension)
        item['remote_version'] = extension.remote.version
        return item

    @property
    def selected_extensions(self):
        return [e['self'] for e in self.selected]

    @property
    def selected(self):
        return [row for row in self.get() if row['install']]
