from django.db import models

from hotel.models.place import ClassInfo

class Service(models.Model):
    service_description = models.TextField("Описание услуги")
    service_price = models.DecimalField("Стоимость услуги", max_digits=8, decimal_places=2)
    classes = models.ManyToManyField(ClassInfo, related_name="services")

    def __str__(self) -> str:
        return self.service_description
    
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"