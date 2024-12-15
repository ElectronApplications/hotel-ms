from rest_framework import serializers

from hotel.models.gallery import *

class GalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = ["id", "image"]    

class GallerySerializer(serializers.ModelSerializer):
    images = GalleryImageSerializer(many=True)

    class Meta:
        model = Gallery
        fields = ["id", "name", "images"]

class CreateGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ["id", "name"]

class UploadGallerySerializer(serializers.Serializer):
    images = serializers.ListField(child=serializers.ImageField())
    
    def save(self, **kwargs):
        gallery: Gallery = self.instance

        for image in self.validated_data["images"]:
            GalleryImage.objects.create(image=image, gallery=gallery)

        return gallery