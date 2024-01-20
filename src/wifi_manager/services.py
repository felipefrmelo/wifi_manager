from typing import Callable
from wifi_manager.main import Router
from wifi_manager.models import Device
from wifi_manager.repository import Repository


def register_allowed_devices(repository: Repository, device: Device):
    device.allow()
    repository.up_insert_device(device)


def get_allowed_devices(repository: Repository) -> list[Device]:
    return repository.allowed_devices


def block_devices(repository: Repository, devices: list[Device]):
    for device in devices:
        device.block()
        repository.up_insert_device(device)


def get_blocked_devices(repository: Repository) -> list[Device]:
    return repository.blocked_devices


def block_all_devices_connected(repository: Repository, router: Router, get_devices_connect_on_wifi: Callable[[], list[Device]]):

    devices_connected = get_devices_connect_on_wifi()

    allowed_devices = get_allowed_devices(repository)
    blocked_devices = get_blocked_devices(repository)

    devices_to_block = remove_devices_in_list(devices_connected, [
                                              *allowed_devices, *blocked_devices]) + blocked_devices

    block_devices(repository, devices_to_block)
    router.block_devices(devices_to_block)


def remove_devices_in_list(devices: list[Device], devices_to_remove: list[Device]) -> list[Device]:
    return [device for device in devices if device not in devices_to_remove]


def get_all_devices_connected(repository: Repository, get_devices_connect_on_wifi: Callable[[], list[Device]]) -> list[Device]:

    devices_connected = get_devices_connect_on_wifi()

    return [repository.find_device_by_ip_address(
        device.ip_address) or device for device in devices_connected]
