from vanilla import CheckBox

from mechanic.storage import Storage


class SettingCheckBox(CheckBox):

    def __init__(self, bounds, label, key):
        self.key = key
        super(SettingCheckBox, self).__init__(bounds,
                                              label,
                                              value=self.value,
                                              callback=self.save)

    def save(self, sender):
        self.value = sender.get()

    @property
    def value(self):
        return bool(Storage.get(self.key))

    @value.setter
    def value(self, val):
        return Storage.set(self.key, bool(val))
