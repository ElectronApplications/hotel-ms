from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, AllowAny

from hotel.models.client import *
from hotel.serializers.client import *
from hotel.permissions import *

class UserViewSet(
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Client.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == "list":
            self.permission_classes = [IsAuthenticated]
        elif self.action == "create":
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset().first()
        serializer = self.get_serializer(qs)
        return Response(serializer.data)

class ClientViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer