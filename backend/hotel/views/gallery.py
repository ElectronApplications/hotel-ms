from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404

from hotel.permissions import IsPlanningOrReadOnly
from hotel.serializers.gallery import *
from hotel.models.gallery import *

class GalleryViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    queryset = Gallery.objects.all()
    permission_classes = [IsPlanningOrReadOnly]
    serializer_class = GallerySerializer

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return CreateGallerySerializer
        else:
            return super().get_serializer_class()

    @action(detail=True, url_path="upload", methods=["post"], serializer_class=UploadGallerySerializer)
    def upload_images(self, request, *args, **kwargs):
        gallery = self.get_object()
        serializer = self.get_serializer(gallery, data=request.data)
        serializer.is_valid(raise_exception=True)
        gallery = serializer.save()

        self.serializer_class = GallerySerializer
        return Response(self.get_serializer(gallery).data)
    
    @action(detail=True, url_path="(?P<image_pk>[^\/.a-zA-Z]+)", methods=["delete"])
    def remove_image(self, request, image_pk, *args, **kwargs):
        gallery: Gallery = self.get_object()
        gallery_image = get_object_or_404(GalleryImage.objects.filter(gallery=gallery), pk=image_pk)
        gallery_image.delete()

        return Response(self.get_serializer(gallery).data)