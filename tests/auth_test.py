from wifi_manager import auth
from wifi_manager.client import Client
import pytest
import os

password = os.environ['ROUTER_PASSWORD']
login = os.environ['ROUTER_LOGIN']


@pytest.mark.slow
def test_integration_get_access_token():

    access_token = auth.get_access_token(Client(), login, password)

    assert isinstance(access_token, str)
