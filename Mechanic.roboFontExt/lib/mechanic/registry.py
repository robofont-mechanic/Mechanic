import requests

from mechanic.env import default_registry


class Registry(object):

    @classmethod
    def all(self):
        return [extension for url in [default_registry]
                          for extension in Registry(url).get()]

    def __init__(self, base_url):
        self.base_url = base_url

    def get(self):
        print "Mechanic: fetching extensions from %s..." % self.url
        response = requests.get(self.url)
        response.raise_for_status()
        return response.json()

    def add(self, **data):
        print "Mechanic: posting extension to %s..." % self.url
        response = requests.post(self.url, data=data)
        return response

    @property
    def url(self):
        return self.base_url + "/api/v1/registry.json"
