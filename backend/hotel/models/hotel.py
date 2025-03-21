from django.db import models

from hotel.models.gallery import Gallery

class ClassInfo(models.Model):
    class_description = models.TextField("Class description")
    place_price = models.DecimalField("Price of a place", max_digits=14, decimal_places=2)
    gallery = models.ForeignKey(Gallery, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.class_description

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"

class Service(models.Model):
    service_description = models.TextField("Service description")
    service_price = models.DecimalField("Service price", max_digits=14, decimal_places=2)
    classes = models.ManyToManyField(ClassInfo, related_name="services")
    gallery = models.ForeignKey(Gallery, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.service_description
    
    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"

class Room(models.Model):
    room_class = models.ForeignKey(ClassInfo, on_delete=models.PROTECT, null=False, related_name="rooms")
    room_number = models.IntegerField("Physical room number", unique=True)
    places = models.IntegerField("The amount of places")

    class Status(models.TextChoices):
        FREE = "free", "Free"
        NOTREADY = "notready", "Not ready"
        TAKEN = "taken", "Taken"
    status = models.CharField(max_length=8, choices=Status.choices, default=Status.FREE)

    def __str__(self) -> str:
        return f"Room {str(self.id)} - {str(self.room_class.class_description)}"
    
    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"