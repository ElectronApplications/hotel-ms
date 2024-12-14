from rest_framework import serializers
from hotel.models.reservation import *

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["id", "room", "move_in_time", "move_out_time", "client"]
