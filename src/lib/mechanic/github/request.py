import requests

from mechanic import logger


class GithubRequest(object):

    __cache = {}

    def __init__(self, url):
        self.url = url

    def get(self):
        logger.debug('Requesting {}'.format(self.url))

        return self.cache_response(self.url, self.get_with_etag_cache(self.url))

    def get_with_etag_cache(self, url):
        headers = {}
        cached_response = self.cache.get(url, None)

        if cached_response is not None:
            etag = self.get_etag(cached_response)
            headers['If-None-Match'] = etag

        logger.debug('Headers: %s', headers)

        response = requests.get(url, headers=headers, auth=NullAuth())

        self.log_header(response, 'x-ratelimit-limit')
        self.log_header(response, 'x-ratelimit-remaining')

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

    def log_header(self, response, key):
        if key in response.headers:
            logger.debug('%s: %s', key, response.headers[key])

    @property
    def cache(self):
        return self.__class__.__cache


class NullAuth(requests.auth.AuthBase):
    '''force requests to ignore the ``.netrc``

    Copied from: https://github.com/kennethreitz/requests/issues/2773#issuecomment-174312831

    Some sites do not support regular authentication, but we still
    want to store credentials in the ``.netrc`` file and submit them
    as form elements. Without this, requests would otherwise use the
    .netrc which leads, on some sites, to a 401 error.

    Use with::

        requests.get(url, auth=NullAuth())
    '''

    def __call__(self, r):
        return r
