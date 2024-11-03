from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, PasswordField
from typing import Any, Dict

from hotel.models.client import Client

class ClientTokenObtainSerializer(TokenObtainPairSerializer):
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