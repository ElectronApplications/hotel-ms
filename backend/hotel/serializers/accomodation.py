from rest_framework import serializers
from hotel.models.accomodation import *

class AccomodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accomodation
        fields = ["id", "move_in_time", "move_out_time", "client", "places", "price_to_pay", "was_price_paid", "checked_out", "reservation"]

class ServiceCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCard
        fields = ["id", "service", "accomodation", "price_to_pay", "was_price_paid", "service_time"]