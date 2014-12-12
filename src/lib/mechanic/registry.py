import requests

from mechanic.env import default_registry
from mechanic.storage import Storage


class Registry(object):

    def __init__(self, base_url=default_registry):
        self.base_url = base_url

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
        return self.base_url + "/api/v1/registry.json"
