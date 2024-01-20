from typing import Protocol
from wifi_manager.auth import get_access_token
from wifi_manager.client import Client
from wifi_manager.models import Device
import os

password = os.environ['ROUTER_PASSWORD']
login = os.environ['ROUTER_LOGIN']

BASE_URL = 'http://192.168.0.1/api/v1'


class Router(Protocol):
    def block_devices(self, devices: list[Device]):
        ...


class RouterClaro(Router):
    def __init__(self, client: Client):
        self.client = client

    def block_devices(self, devices: list[Device]):
        response = self.client.put(
            f'/service/macFiltering?_={self.client.get_timestamp()}',
            json={
                "rules": [
                    {
                        "macAddress": device.mac_address,
                        "active": 'true',

                    }
                    for device in devices
                ]

            },
        )
        return response


def factory_router() -> Router:
    access_token = get_access_token(Client(), login, password)
    client = Client(base_url=BASE_URL, access_token=access_token)
    return RouterClaro(client)


def main():
    pass
