import requests

from mechanic.storage import Storage


class Registry(object):

    def all(self):
        print "Mechanic: fetching extensions from %s..." % self.url

        response = requests.get(self.url)
        response.raise_for_status()
        return response.json()

    def add(self, **data):
        response = requests.post(self.url, data=data)
        return response

    @property
    def url(self):
        return Storage.get('registries')[0] + "/api/v1/registry.json"
