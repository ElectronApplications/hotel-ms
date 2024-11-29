from django.db import models

class ClassInfo(models.Model):
    class_description = models.TextField("Class description")
    place_price = models.DecimalField("Price of a place", max_digits=8, decimal_places=2)

    def __str__(self) -> str:
        return self.class_description

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"

class Room(models.Model):
    room_class = models.ForeignKey(ClassInfo, on_delete=models.PROTECT, null=False, related_name="rooms")

    def __str__(self) -> str:
        return f"Room {str(self.id)} - {str(self.room_class)}"
    
    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"

class Place(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False, related_name="places")

    class Status(models.TextChoices):
        FREE = "free", "Free"
        UNREADY = "notready", "Not ready"
        TAKEN = "taken", "Taken"
    status = models.CharField(max_length=8, choices=Status.choices, default=Status.FREE)

    def __str__(self) -> str:
        return f"Place {str(self.id)} in room {str(self.room.id)} - {str(self.room.room_class)}"

    class Meta:
        verbose_name = "Place"
        verbose_name_plural = "Places"

class Service(models.Model):
    service_description = models.TextField("Service description")
    service_price = models.DecimalField("Service price", max_digits=8, decimal_places=2)
    classes = models.ManyToManyField(ClassInfo, related_name="services")

    def __str__(self) -> str:
        return self.service_description
    
    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"