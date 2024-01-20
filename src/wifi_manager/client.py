
from dataclasses import dataclass
import requests
import time


@dataclass
class Response:
    status: str
    data: dict


class Client:

    def __init__(self, base_url='http://192.168.0.1/api/v1', access_token=None):
        self.base_url = base_url
        self.access_token = access_token

    def get(self, url, **kwargs):
        r = requests.get(self.base_url + url, **self.merge_headers(kwargs))
        return self._response(r)

    def post(self, url, **kwargs):
        r = requests.post(self.base_url + url, **self.merge_headers(kwargs))
        return self._response(r)

    def put(self, url, **kwargs):
        r = requests.put(self.base_url + url, **self.merge_headers(kwargs))
        return self._response(r)

    def merge_headers(self, kwargs):
        return {**kwargs, 'headers': {
            **kwargs.get('headers', {}),
            "Access-Token": self.access_token,
        }}

    def set_access_token(self, access_token):
        self.access_token = access_token

    def _response(self, response):
        return Response(
            status=response.status_code,
            data=response.json()
        )

    def get_timestamp(self):
        MILISECONDS = 1000
        return int(time.time() * MILISECONDS)
