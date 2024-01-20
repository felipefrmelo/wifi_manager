from django.shortcuts import redirect, render
from wifi_manager.auth import get_access_token
from wifi_manager.main import BASE_URL, RouterClaro, factory_router
from wifi_manager.network import get_devices_connect_on_wifi
from wifi_manager.services import block_all_devices_connected, block_devices, get_all_devices_connected, register_allowed_devices
from .models import RepositoryDjango, DeviceDjango
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm, widgets, TextInput


def textInput(readonly=True): return TextInput(
    attrs={'class': 'mb-2 bg-gray-100 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500' + (' cursor-not-allowed' if readonly else ''), 'readonly': readonly})


checkBox = widgets.CheckboxInput(
    attrs={'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600', 'disabled': True})


class DeviceForm(ModelForm):

    class Meta:
        model = DeviceDjango
        fields = '__all__'
        labels = {
            'ip_address': 'IP Address',
            'mac_address': 'MAC Address',
            'owner': 'Owner',
            'blocked': 'Blocked',
            'name': 'Name',
        }
        widgets = {
            'ip_address': textInput(),
            'mac_address': textInput(),
            'owner': textInput(False),
            'blocked': checkBox,
            'name': textInput(False),
        }

    def to_domain(self):
        return DeviceDjango(
            ip_address=self.cleaned_data['ip_address'],
            owner=self.cleaned_data['owner'],
            blocked=self.cleaned_data['blocked'],
            name=self.cleaned_data['name']
        ).to_domain()


@login_required(login_url='/admin/login/')
def index(request):
    repository = RepositoryDjango()

    devices_connected = get_all_devices_connected(
        repository, get_devices_connect_on_wifi)

    devicesForm = [DeviceForm(instance=DeviceDjango.from_domain(device))
                   for device in devices_connected]
    return render(request, 'wifi/index.html', {'devices': devicesForm, 'devices_connected': len(devices_connected)})


@login_required(login_url='/admin/login/')
def register_device(request):
    if request.method == 'POST':
        ip_address = request.POST['ip_address']
        mac_address = request.POST['mac_address']
        owner = request.POST['owner']
        name = request.POST['name']

        device = DeviceDjango(
            ip_address=ip_address,
            mac_address=mac_address,
            owner=owner,
            blocked=False,
            name=name
        )
        register_allowed_devices(RepositoryDjango(), device.to_domain())

    return redirect('index')


@login_required(login_url='/admin/login/')
def devices_allowed(request):
    repository = RepositoryDjango()

    return render(request, 'wifi/devices_allowed.html', {'devices': repository.allowed_devices, 'devices_allowed': len(repository.allowed_devices)})


@login_required(login_url='/admin/login/')
def devices_blocked(request):
    repository = RepositoryDjango()

    return render(request, 'wifi/devices_blocked.html', {'devices': repository.blocked_devices, 'devices_blocked': len(repository.blocked_devices)})


@login_required(login_url='/admin/login/')
def allow_device(request, ip_address):
    repository = RepositoryDjango()

    device = repository.find_device_by_ip_address(ip_address)
    if device is not None:
        register_allowed_devices(repository, device)

    return redirect('devices_blocked')


@login_required(login_url='/admin/login/')
def remove_device(request, ip_address):
    repository = RepositoryDjango()

    device = repository.find_device_by_ip_address(ip_address)
    print(device)
    if device is not None:
        block_devices(repository, [device])

    return redirect('devices_allowed')



@login_required(login_url='/admin/login/')
def block_all_devices(request):
    repository = RepositoryDjango()
    router = factory_router()
    block_all_devices_connected(repository, router, get_devices_connect_on_wifi)

    return redirect('index')
