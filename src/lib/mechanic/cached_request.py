import requests


class CachedRequest(object):

    __cache = {}

    def __init__(self, url):
        self.url = url

    def get(self):
        response = requests.get(self.url)
        response.raise_for_status()
        return response
