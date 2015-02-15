import fnmatch
import requests


class GithubTree(object):

    api = 'https://api.github.com/repos/%(repo)s/git/trees/HEAD?recursive=1'

    def __init__(self, repository):
        response = requests.get(self.endpoint(repository))
        self.files = response.json().get('tree', [])

    def endpoint(self, repository):
        return self.api % {'repo': repository}

    def find(self, filename):
        glob = '*%s' % filename
        finder = (f for f in self.files if fnmatch.fnmatch(f['path'], glob))
        return next(finder, None)
