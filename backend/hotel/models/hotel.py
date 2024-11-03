from django.db import models

class ClassInfo(models.Model):
    class_description = models.TextField("Описание класса")
    place_price = models.DecimalField("Стоимость места", max_digits=8, decimal_places=2)

    def __str__(self) -> str:
        return self.class_description

    class Meta:
        verbose_name = "Класс"
        verbose_name_plural = "Классы"

class Room(models.Model):
    room_class = models.ForeignKey(ClassInfo, on_delete=models.PROTECT, null=False, related_name="rooms")

    def __str__(self) -> str:
        return f"Комната {str(self.id)} - {str(self.room_class)}"
    
    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"

class Place(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False, related_name="places")

    class Status(models.TextChoices):
        FREE = "free", "Свободно"
        UNREADY = "unready", "Не готово"
        TAKEN = "taken", "Занято"
    status = models.CharField(max_length=8, choices=Status.choices, default=Status.FREE)

    def __str__(self) -> str:
        return f"Место {str(self.id)} в комнате {str(self.room.id)} - {str(self.room.room_class)}"

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

class Service(models.Model):
    service_description = models.TextField("Описание услуги")
    service_price = models.DecimalField("Стоимость услуги", max_digits=8, decimal_places=2)
    classes = models.ManyToManyField(ClassInfo, related_name="services")

    def __str__(self) -> str:
        return self.service_description
    
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"