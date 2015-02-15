import requests

from mechanic import logger


class GithubRequest(object):

    __cache = {}

    def __init__(self, url):
        self.url = url

    def get(self):
        logger.info('Requesting {}'.format(self.url))
        return self.cache_response(self.url, self.get_cached(self.url))

    def get_cached(self, url):
        headers = {}
        cached_response = self.cache.get(url, None)

        if cached_response is not None:
            etag = self.get_etag(cached_response)
            headers['If-None-Match'] = etag

        response = requests.get(url, headers=headers)

        if response.status_code == 304:
            logger.info('Using cached response for {}'.format(self.url))
            response = cached_response

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
