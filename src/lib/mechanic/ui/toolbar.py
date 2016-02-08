class Toolbar(object):

    def __init__(self, window):
        self.items = []
        self.window = window

    def index_of(self, identifier):
        return next((index for index, item
                           in enumerate(self.items)
                           if item['itemIdentifier'] == identifier), 0)

    def add(self, view):
        item = dict(itemIdentifier=view.identifier,
                    label=view.title,
                    callback=self.window.toolbar_select,
                    imageNamed=view.image,
                    selectable=True,
                    view=view)
        self.items.append(item)

    @property
    def labels(self):
        return [item['label'] for item in self.items]

