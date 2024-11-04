from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import mixins
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from hotel.models.client import *
from hotel.serializers.client import *
from hotel.permissions import *

class UserViewSet(
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Client.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    @action(detail=False, url_path="self", methods=["get"], permission_classes=[IsAuthenticated])
    def get_self(self, request, *args, **kwargs):
        client = self.get_queryset().first()
        serializer = self.get_serializer(client)
        return Response(serializer.data)

    @action(detail=False, url_path="password", methods=["put"], permission_classes=[IsAuthenticated], serializer_class=UserChangePasswordSerializer)
    def change_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, url_path="name", methods=["put"], permission_classes=[IsAuthenticated], serializer_class=UserChangeNameSerializer)
    def change_name(self, request, *args, **kwargs):
        client = self.get_queryset().first()
        serializer = self.get_serializer(client, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

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