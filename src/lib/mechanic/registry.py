import requests

from mechanic.env import default_registry
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
        return default_registry + "/api/v1/registry.json"
