from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from hotel.models.client import *
from hotel.serializers.client import *

class UserViewSet(
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Client.objects.all()
    serializer_class = UserSerializer

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