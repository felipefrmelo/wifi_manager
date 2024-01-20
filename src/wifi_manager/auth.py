from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64

from wifi_manager.client import Client


def get_access_token(client: Client, username, password):
    key = get_key(client)
    password_hash = get_password_hash(key, username, password)

    response = client.post(
        '/gateway/users/login',
        json={
            'userName': username,
            'password': password_hash,
        },
    )
    return response.data['accessToken']


def get_key(client: Client):

    response = client.get(
        f'/gateway/users/login/auth?_={client.get_timestamp()}'
    )
    return response.data['web_key']


def get_password_hash(key, username, password):
    algorithm = hashes.SHA512()
    kdf = PBKDF2HMAC(
        algorithm=algorithm,
        length=32,
        salt=bytes(key, 'utf-8'),
        iterations=2048,
    )
    password_hash = kdf.derive(bytes(password, 'utf-8')).hex()

    base64_string = f'HS:{username}:{password_hash}'

    return base64.b64encode(base64_string.encode('utf-8')).decode('utf-8')
