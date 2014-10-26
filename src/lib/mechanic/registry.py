import requests


class Registry(object):
    registry_url = "http://www.robofontmechanic.com/api/v1/registry.json"

    def __init__(self, url=None):
        if url is not None:
            self.registry_url = url

    def all(self):
        response = requests.get(self.registry_url)
        response.raise_for_status()
        return response.json()

    def add(self, **data):
        response = requests.post(self.registry_url, data=data)
        return response
