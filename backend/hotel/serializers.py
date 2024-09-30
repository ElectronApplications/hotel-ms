from rest_framework import serializers

from hotel.models.client import Client
from hotel.models.reservation import Reservation

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "name", "phone_number"]

class ReservationSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    
    class Meta:
        model = Reservation
        fields = ["id", "move_in_time", "move_out_time", "client"]