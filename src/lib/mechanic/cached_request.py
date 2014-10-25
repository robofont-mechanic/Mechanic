import requests


class CachedRequest(object):

    __cache = {}

    def __init__(self, url):
        self.url = url

    def get(self):
        return self.cache_response(self.url, self.get_cached(self.url))

    def get_cached(self, url):
        cached_response = self.cache.get(url, None)
        if cached_response is not None:
            etag = self.get_etag(cached_response)
            response = requests.get(url, headers={'If-None-Match': etag})
            if response.status_code is 304:
                response = cached_response
        else:
            response = requests.get(url)
        response.raise_for_status()
        return response

    def cache_response(self, url, response):
        if self.get_etag(response):
            self.cache[url] = response
        return response

    def get_etag(self, response):
        return response.headers['ETag']

    @property
    def cache(self):
        return self.__class__.__cache
