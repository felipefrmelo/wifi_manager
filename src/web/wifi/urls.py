from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register_device", views.register_device, name="register_device"),
    path("devices_allowed", views.devices_allowed, name="devices_allowed"),
    path("devices_blocked", views.devices_blocked, name="devices_blocked"),
    path("remove_device/<str:ip_address>", views.remove_device, name="remove_device"),
    path("allow_device/<str:ip_address>", views.allow_device, name="allow_device"),
    path("block_all_devices_connected", views.block_all_devices, name="block_all_devices_connected"),
]
