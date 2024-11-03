from rest_framework import serializers
from hotel.models.client import *

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "name", "phone_number", "user"]