from rest_framework import serializers
from hotel.models.hotel import *

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