from wifi_manager.models import Device
from wifi_manager.network import get_devices_connect_on_wifi, meu_ip, router_ip
import pytest


@pytest.mark.slow
def test_get_devices_connect_on_wifi():

    devices = get_devices_connect_on_wifi()

    for device in devices:
        assert isinstance(device, Device)

    assert router_ip() in [device.ip_address for device in devices]
