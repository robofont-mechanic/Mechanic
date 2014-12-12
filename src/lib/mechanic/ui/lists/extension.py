from vanilla import List


class ExtensionList(List):

    def _wrapItem(self, extension):
        item = {'name': extension.bundle.name,
                'local_version': extension.config['version'],
                'install': True,
                'check_for_updates': not extension.is_ignored,
                'self': extension}

        return super(ExtensionList, self)._wrapItem(item)
