import os
import subprocess

from wifi_manager.models import Device


def get_devices_connect_on_wifi() -> list[Device]:

    path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'network_scan.sh')

    arp_command = [path]
    output = subprocess.check_output(arp_command).decode()

    devices = [device.split('\t') for device in output.split('\n')[2:-4]]

    return [Device(ip_address=device[0], mac_address=device[1], name=device[2]) for device in devices]


def meu_ip():
    return os.popen("ip route get 8.8.8.8 | awk '{printf $7}'").read().strip()


def router_ip():
    return os.popen("ip route get 8.8.8.8 | awk '{printf $3}'").read().strip()
