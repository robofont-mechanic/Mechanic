from mechanic.ui.lists.base import BaseList


class ExtensionList(BaseList):

    def _wrapItem(self, extension):
        item = {'name': extension.bundle.name,
                'local_version': extension.configuration['version'],
                'install': True,
                'check_for_updates': not extension.is_ignored,
                'self': extension}

        return super(ExtensionList, self)._wrapItem(item)
