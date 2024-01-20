from django.db import models


from django.db import models
from wifi_manager.repository import Repository
from wifi_manager.models import Device


class DeviceDjango(models.Model):
    ip_address = models.CharField(max_length=20, unique=True, primary_key=True)
    mac_address = models.CharField(max_length=20, unique=True)
    owner = models.CharField(max_length=100, default='unknown')
    blocked = models.BooleanField(default=False)  # type: ignore
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'[ip_address: {self.ip_address}, owner: {self.owner}, blocked: {self.blocked}, name: {self.name}, mac_address: {self.mac_address}]'

    def to_domain(self) -> Device:
        return Device(
            ip_address=str(self.ip_address),
            mac_address=str(self.mac_address),
            owner=str(self.owner),
            blocked=bool(self.blocked),
            name=str(self.name)
        )

    @classmethod
    def from_domain(cls, device: Device) -> 'DeviceDjango':
        return cls(
            ip_address=str(device.ip_address),
            mac_address=str(device.mac_address),
            owner=str(device.owner),
            blocked=bool(device.blocked),
            name=str(device.name)
        )


class RepositoryDjango(Repository):

    def up_insert_device(self, device: Device):
        DeviceDjango.objects.update_or_create(
            ip_address=device.ip_address,
            mac_address=device.mac_address,
            defaults={
                'owner': device.owner,
                'blocked': device.blocked,
                'name': device.name
            }
        )

    @property
    def allowed_devices(self) -> list[Device]:
        return [device.to_domain() for device in DeviceDjango.objects.all() if not device.blocked] # type: ignore

    @property
    def blocked_devices(self) -> list[Device]:
        return [device.to_domain() for device in DeviceDjango.objects.all() if device.blocked] # type: ignore

    def find_device_by_ip_address(self, ip_address: str) -> Device | None:
        try:
            return DeviceDjango.objects.get(ip_address=ip_address).to_domain() # type: ignore
        except DeviceDjango.DoesNotExist:  # type: ignore
            return None
