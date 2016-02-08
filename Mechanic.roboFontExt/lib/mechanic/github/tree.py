import fnmatch

from .request import GithubRequest


TREE_URL = 'https://api.github.com/repos/%(repo)s/git/trees/HEAD?recursive=1'


class GithubTree(object):

    def __init__(self, repository):
        response = GithubRequest(self.endpoint(repository)).get()
        self.files = response.json().get('tree', [])

    def endpoint(self, repository):
        return TREE_URL % {'repo': repository}

    def find(self, filename):
        glob = '*%s' % filename
        finder = (f for f in self.files if fnmatch.fnmatch(f['path'], glob))
        return next(finder, None)
