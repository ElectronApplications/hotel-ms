from rest_framework import serializers
from rest_framework_simplejwt.serializers import PasswordField
from hotel.models.client import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = PasswordField()

    class Meta:
        model = Client
        fields = ["id", "name", "phone_number", "password", "role"]
        read_only_fields = ["role"]

    def validate_phone_number(self, phone_number: str) -> str:  
        existing_client = Client.objects.filter(phone_number=phone_number).first()
        if existing_client is not None and existing_client.user is not None:
            raise serializers.ValidationError("User with the given phone number already exists")
        
        return phone_number

    def create(self, validated_data: dict):
        print(validated_data)
        phone_number = validated_data.pop("phone_number")

        user = User.objects.create_user(username=phone_number, password=validated_data.pop("password"))
        validated_data["user"] = user

        client, created = Client.objects.update_or_create(phone_number=phone_number, defaults=validated_data)
        return client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "name", "phone_number", "user"]