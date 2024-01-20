from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class IndexViewTest(TestCase):

    def setUp(self):
        User = get_user_model()
        User.objects.create_user(
            'temporary', 'temporary@gmail.com', 'temporary')
        self.client.login(username='temporary', password='temporary')

    def test_index_view(self):

        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'IP Address')
        self.assertContains(response, 'Owner')
        self.assertContains(response, 'Blocked')
        self.assertContains(response, 'Name')
        self.assertContains(response, 'Allow Access')

    def test_register_device(self):
        response = self.post_device()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def post_device(self):
        return self.client.post(reverse("register_device"), {
            'ip_address': '192.168.0.1',
            'owner': 'OwnerTest',
            'name': 'NameTest',
        })

    def test_devices_allowed(self):

        self.post_device()

        response = self.client.get(reverse("devices_allowed"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'OwnerTest')
        self.assertContains(response, 'NameTest')

    def test_remove_device(self):

        self.post_device()

        self.client.get(reverse("remove_device", kwargs={
                        'ip_address': '192.168.0.1'}))

        response = self.client.get(reverse("devices_allowed"))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'OwnerTest')
        self.assertNotContains(response, 'NameTest')
