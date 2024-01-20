from typing import Protocol
from wifi_manager.models import Device


class Repository(Protocol):

    def up_insert_device(self, device: Device):
        ...

    @property
    def allowed_devices(self) -> list[Device]:
        ...

    @property
    def blocked_devices(self) -> list[Device]:
        ...

    def find_device_by_ip_address(self, ip_address: str) -> Device | None:
        ...


class RepositoryInMemory(Repository):

    def __init__(self) -> None:
        self._devices = []

    def up_insert_device(self, device: Device):
        self._devices = [
            *filter(lambda d: d.ip_address != device.ip_address, self._devices), device]

    @property
    def allowed_devices(self) -> list[Device]:
        return list(filter(lambda d: not d.blocked, self._devices))

    @property
    def blocked_devices(self) -> list[Device]:
        return list(filter(lambda d: d.blocked, self._devices))

    def find_device_by_ip_address(self, ip_address: str) -> Device | None:
        return next(filter(lambda d: d.ip_address == ip_address, self._devices), None)
