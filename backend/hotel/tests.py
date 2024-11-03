from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker

from hotel.models.hotel import ClassInfo, Service
from hotel.models.client import Client

# Create your tests here.

class ClientViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_client(self):
        r = self.client.post("/api/client/", {
            "name": "Foobar Foobarovich",
            "phone_number": "88005553535"
        })
        client_id = r.json()["id"]

        assert Client.objects.count() == 1

        new_client = Client.objects.filter(id=client_id).first()
        assert new_client.name == "Foobar Foobarovich"
        assert new_client.phone_number == "88005553535"
    
    def test_service(self):
        class_info = baker.make(ClassInfo)
        r = self.client.post("/api/service/", {
            "service_description": "Test service",
            "service_price": "1000.00",
            "classes": [class_info.id]
        })
        service = r.json()
        assert service["service_price"] == "1000.00"

        r = self.client.put(f"/api/service/{service["id"]}/", {
            "service_description": "Test service",
            "service_price": "500.00",
            "classes": [class_info.id]
        })
        service = r.json()
        assert service["service_price"] == "500.00"
        
        self.client.delete(f"/api/service/{service["id"]}/")

        assert Service.objects.count() == 0