from vanilla import List


class BaseList(List):

    def __init__(self, *args, **kwargs):
        kwargs['columnDescriptions'] = self.columns
        super(BaseList, self).__init__(*args, **kwargs)
