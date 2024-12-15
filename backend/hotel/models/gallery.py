from django.db import models

class Gallery(models.Model):
    name = models.TextField("Gallery name")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Gallery"
        verbose_name_plural = "Galleries"

class GalleryImage(models.Model):
    image = models.ImageField("Gallery image", upload_to="gallery")
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, null=False, related_name="images")

    def __str__(self) -> str:
        return self.image.name

    class Meta:
        verbose_name = "Gallery image"
        verbose_name_plural = "Gallery images"