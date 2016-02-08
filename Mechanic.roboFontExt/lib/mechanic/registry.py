import requests

from mechanic import env, logger


class Registry(object):

    class ConnectionError(Exception): pass

    @classmethod
    def all(self):
        return [extension for url in [env.default_registry]
                          for extension in Registry(url).extensions()]

    def __init__(self, base_url):
        self.base_url = base_url

    def extensions(self):
        logger.info("fetching extensions from %s..." % self.base_url)
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.json()
        except requests.ConnectionError:
            raise Registry.ConnectionError

    def add(self, **data):
        logger.info("posting extension to %s..." % self.base_url)
        return requests.post(self.url, data=data)

    @property
    def url(self):
        return self.base_url + "/api/v1/registry.json"
