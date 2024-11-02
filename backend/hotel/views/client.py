from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from hotel.models.client import Client
from hotel.serializers import ClientSerializer

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