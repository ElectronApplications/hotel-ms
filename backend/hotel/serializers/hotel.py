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
        fields = ["id", "room_number", "room_class", "status", "places"]

    def validate_places(self, places: int):
        if places < 1:
            raise serializers.ValidationError("Amount of places can't be negative or zero")

        return places

class CleaningRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "room_number", "room_class", "status", "places"]
        read_only_fields = ["room_number", "room_class", "places"]
    
    def validate_status(self, status: Room.Status):
        if status != Room.Status.FREE:
            raise serializers.ValidationError("You can only change rooms' status to 'free'")
        
        if self.instance is not None and self.instance.status != Room.Status.NOTREADY:
            raise serializers.ValidationError("You can only change rooms with 'notready' status")
        
        return status

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "service_description", "service_price", "classes"]
    
    def validate_service_price(self, service_price: float):
        if service_price < 0:
            raise serializers.ValidationError("Price can't be negative")
    
        return service_price