from rest_framework import serializers
from hotel.models.hotel import *

class ClassInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassInfo
        fields = ["id", "class_description", "place_price"]
    
    def validate_place_price(self, place_price: float):
        if place_price < 0:
            raise serializers.ValidationError("Price can't be negative")
        
        return place_price

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
    
    def validate_service_price(self, service_price: float):
        if service_price < 0:
            raise serializers.ValidationError("Price can't be negative")
    
        return service_price