from typing import Any, Dict
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer, PasswordField

from hotel.models.accomodation import Accomodation, ServiceCard
from hotel.models.service import Service
from hotel.models.place import ClassInfo, Place, Room
from hotel.models.client import Client
from hotel.models.reservation import Reservation

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "name", "phone_number", "user"]

class ClassInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassInfo
        fields = ["id", "class_description", "place_price"]

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "room_class"]

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ["id", "room"]

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "service_description", "service_price", "classes"]

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["id", "move_in_time", "move_out_time", "client", "places"]

class AccomodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accomodation
        fields = ["id", "move_in_time", "move_out_time", "client", "places", "price_to_pay", "was_price_paid", "checked_out", "reservation"]

class ServiceCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCard
        fields = ["id", "service", "accomodation", "price_to_pay", "was_price_paid", "service_time"]

class ClientTokenObtainSerializer(TokenObtainSerializer):
    def __init__(self, *args, **kwargs) -> None:
        serializers.Serializer.__init__(self, *args, **kwargs)

        self.fields["phone_number"] = serializers.CharField(write_only=True)
        self.fields["password"] = PasswordField()

    def validate(self, attrs: Dict[str, Any]) -> Dict[Any, Any]:
        client = Client.objects.filter(phone_number=attrs["phone_number"]).first()

        if client is None or client.user is None:
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        attrs[self.username_field] = client.user.username
        return super().validate(attrs)