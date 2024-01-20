import pytest
from wifi_manager.main import Router
from wifi_manager.models import Device
from wifi_manager.repository import Repository, RepositoryInMemory
from wifi_manager.services import register_allowed_devices, get_allowed_devices, block_devices, get_blocked_devices, block_all_devices_connected, get_all_devices_connected
from faker import Faker

fake = Faker()


class FakeRouter(Router):

    def __init__(self):
        self.devices = []

    def block_devices(self, devices: list[Device]):
        self.devices = devices


@pytest.fixture
def repository():
    return RepositoryInMemory()


def test_register_allowed_devices(repository: Repository):
    device = make_device()

    register_allowed_devices(repository, device)

def make_device():
    device = Device(owner=fake.name(), ip_address=fake.ipv4(), mac_address=fake.mac_address(), name=fake.name())
    return device


def test_get_allowed_devices(repository: Repository):
    device = make_device()

    register_allowed_devices(repository, device)

    assert device in get_allowed_devices(repository)


def test_get_allowed_devices_empty(repository: Repository):

    assert get_allowed_devices(repository) == []


def test_block_devices(repository: Repository):
    device = make_device()

    block_devices(repository, [device])

    assert device.blocked
    assert device in get_blocked_devices(repository)


def test_block_and_allow_devices(repository: Repository):
    device_blocked = make_device()
    device_allowed = make_device()

    block_devices(repository, [device_blocked])
    register_allowed_devices(repository, device_allowed)

    assert device_blocked in get_blocked_devices(repository)
    assert device_blocked not in get_allowed_devices(repository)

    assert device_allowed in get_allowed_devices(repository)
    assert device_allowed not in get_blocked_devices(repository)


def test_register_and_block_same_device(repository: Repository):
    device = make_device()

    register_allowed_devices(repository, device)
    block_devices(repository, [device])
    register_allowed_devices(repository, device)

    assert [device] == get_allowed_devices(repository)
    assert [] == get_blocked_devices(repository)


def test_block_all_devices_connected(repository: Repository):
    device_blocked = make_device()
    device_allowed = make_device()
    unknown_device = Device(ip_address=fake.ipv4(), mac_address=fake.mac_address())

    block_devices(repository, [device_blocked])
    register_allowed_devices(repository, device_allowed)

    def get_devices_connect_on_wifi(): return [
        device_blocked, device_allowed, unknown_device]

    router = FakeRouter()

    block_all_devices_connected(
        repository, router, get_devices_connect_on_wifi)

    assert len(router.devices) == 2
    for device in [device_blocked, unknown_device]:
        assert device in router.devices


def test_block_all_devices_connected_and_blocked_devices(repository: Repository):
    device_blocked = make_device()
    device_allowed = make_device()
    unknown_device = Device(ip_address=fake.ipv4(), mac_address=fake.mac_address())

    block_devices(repository, [device_blocked])
    register_allowed_devices(repository, device_allowed)

    def get_devices_connect_on_wifi(): return [
        device_allowed, unknown_device]

    router = FakeRouter()

    block_all_devices_connected(
        repository, router, get_devices_connect_on_wifi)

    assert len(router.devices) == 2

    for device in [device_blocked, unknown_device]:
        assert device in router.devices


def test_get_all_devices_connected(repository: Repository):
    device_blocked = make_device()
    device_allowed = make_device()
    unknown_device = Device(ip_address=fake.ipv4(), mac_address=fake.mac_address())

    block_devices(repository, [device_blocked])
    register_allowed_devices(repository, device_allowed)

    def get_devices_connect_on_wifi(): return [
        device_allowed, unknown_device, device_blocked]

    devices = get_all_devices_connected(
        repository, get_devices_connect_on_wifi)

    assert len(devices) == 3

    for device in [device_blocked, unknown_device, device_allowed]:
        assert device in devices
