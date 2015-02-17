from vanilla import Group, TextBox, EditText


class TextField(Group):

    indent = 90

    def __init__(self, position, label, placeholder=""):
        super(TextField, self).__init__((position[0], position[1], position[2], 22))

        self.label = TextBox((0, 3, self.indent - 10, 22),
                             "{0}:".format(label),
                             alignment="right")

        self.text = EditText((self.indent, 0, 500 - 40 - self.indent, 22),
                             placeholder=placeholder)

    def set(self, *args):
        return self.text.set(*args)

    def get(self):
        return self.text.get()
