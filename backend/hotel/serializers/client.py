from rest_framework import serializers
from rest_framework_simplejwt.serializers import PasswordField
from hotel.models.client import *
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    password = PasswordField()
    phone_number = serializers.CharField(max_length=16, validators=[RegexValidator(r"^[+][\d]{7,15}$")])

    class Meta:
        model = Client
        fields = ["id", "name", "phone_number", "password", "role", "picture"]
        read_only_fields = ["role", "picture"]

    def validate_phone_number(self, phone_number: str) -> str:  
        existing_client = Client.objects.filter(phone_number=phone_number).first()
        if existing_client is not None and existing_client.user is not None:
            raise serializers.ValidationError("User with the given phone number already exists")
        
        return phone_number

    def create(self, validated_data: dict):
        phone_number = validated_data.pop("phone_number")
        password=validated_data.pop("password")

        validate_password(password)
        user = User.objects.create_user(username=phone_number, password=password)
        validated_data["user"] = user

        client, created = Client.objects.update_or_create(phone_number=phone_number, defaults=validated_data)
        return client

class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, old_password: str) -> str:
        user: User = self.context["request"].user
        if not user.check_password(old_password):
            raise serializers.ValidationError("Incorrect old password")
        
        return old_password

    def validate_new_password(self, new_password: str) -> str:
        validate_password(new_password)
        return new_password

    def save(self, **kwargs):
        user: User = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user

class UserChangeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["name"]

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "name", "phone_number", "role", "user", "picture"]
        read_only_fields= ["role", "user"]
    
    def update(self, instance, validated_data):
        instance: Client = super().update(instance, validated_data)
        if instance.user is not None:
            instance.user.username = instance.phone_number
        return instance

class AdminClientSerializer(ClientSerializer):
    class Meta:
        model = Client
        fields = ["id", "name", "phone_number", "role", "user", "picture"]
        read_only_fields= ["user"]