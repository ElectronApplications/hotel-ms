from django.test import TestCase
import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from hotel.models.hotel import ClassInfo, Service
from hotel.models.client import Client

class ClientModelTestCase(TestCase):
    def test_phone_number_valid(self):
        # None of these should raise an exception
        baker.make(Client, phone_number="+78005553535").full_clean()
        baker.make(Client, phone_number="+1234567").full_clean()
        baker.make(Client, phone_number="+123456789112345").full_clean()
    
    def test_phone_number_invalid(self):
        with pytest.raises(Exception):
            baker.make(Client, phone_number="88005553535").full_clean()
        with pytest.raises(Exception):
            baker.make(Client, phone_number="8-800-555-35-35").full_clean()
        with pytest.raises(Exception):
            baker.make(Client, phone_number="+7(800)555-35-35").full_clean()
        with pytest.raises(Exception):
            baker.make(Client, phone_number="NaPN (not a phone number)").full_clean()
        with pytest.raises(Exception):
            baker.make(Client, phone_number="+123456").full_clean()
        with pytest.raises(Exception):
            baker.make(Client, phone_number="+1234567891123456").full_clean()

class UserViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_register(self):
        r = self.client.post("/api/user/", {
            "name": "Foobar Foobarovich",
            "phone_number": "+78005553535",
            "password": "difficult_password"
        })
        client_id = r.json()["id"]
        client = Client.objects.filter(id=client_id).first()

        assert client is not None
        assert client.phone_number == "+78005553535"
        assert client.user is not None
        assert client.user.check_password("difficult_password")
    
    def test_register_existing(self):
        client_old = Client.objects.create(name="Oldbar Oldbarovich", phone_number="+78005553535")

        r = self.client.post("/api/user/", {
            "name": "Foobar Foobarovich",
            "phone_number": "+78005553535",
            "password": "more_difficult_password"
        })
        print(r.json())
        client_id = r.json()["id"]

        assert client_id == client_old.id

        client = Client.objects.filter(id=client_id).first()

        assert client is not None
        assert client.name == "Foobar Foobarovich"
        assert client.user is not None
        assert client.user.check_password("more_difficult_password")