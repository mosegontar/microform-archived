"""This is a small wrapper for the Mercury Web Parser API.

The code here is basically the same as Kenneth Reitz's mercury-parser
project (https://github.com/kennethreitz/mercury-parser). It is modified
slightly here to simply return a dict representation of the JSON response
from Mercury Web Parser, as well as to make use of requests-cache.
"""
import os
import requests
import requests_cache


MERCURY_DB_NAME = os.environ.get('MERCURY_DB_NAME', 'mercury')
base = os.path.dirname(__file__)
mercury_db = os.path.join([base, MERCURY_DB_NAME]) 

requests_cache.install_cache(
    mercury_db,
    backend='sqlite',
    expire_after = 60*60*24*7*4 # 4 weeks
)


class Mercury(object):

    def __init__(self, api_key):

        self.api_url = 'https://mercury.postlight.com/parser?url='
        self.api_key = api_key
        self.requests = requests.Session()

    def get(self, doc_url, cache_disabled=False):
        headers = {'x-api-key': self.api_key}
        url = self.api_url + doc_url

        if cache_disabled:
            with requests_cache.disabled():
                return self.requests.get(url, headers=headers).json()

        return self.requests.get(url, headers=headers).json()
