from rest_framework import serializers
from hotel.models.accomodation import *
from hotel.serializers.client import ClientSerializer
from hotel.serializers.hotel import RoomSerializer

# TODO: this needs some logic
class AccomodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accomodation
        fields = ["id", "room", "move_in_time", "move_out_time", "client", "price_to_pay", "was_price_paid", "checked_out", "reservation"]

class GetAccomodationSerializer(AccomodationSerializer):
    room = RoomSerializer()
    client = ClientSerializer()

class ServiceCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCard
        fields = ["id", "service", "accomodation", "price_to_pay", "was_price_paid", "service_time"]