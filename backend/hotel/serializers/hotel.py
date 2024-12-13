from rest_framework import serializers
from hotel.models.hotel import *

class ClassInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassInfo
        fields = ["id", "class_description", "place_price"]
        extra_kwargs = {"class_description": {"required": False}, "place_price": {"required": False}}

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "room_class"]

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ["id", "room", "status"]

class CleaningPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ["id", "room", "status"]
        read_only_fields = ["room"]

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "service_description", "service_price", "classes"]