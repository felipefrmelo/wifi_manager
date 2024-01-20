
from wifi_manager.client import Client
import pytest


@pytest.mark.slow
def test__put_devices():
    client = Client()

