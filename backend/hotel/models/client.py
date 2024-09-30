from django.db import models

class Client(models.Model):
    name = models.TextField("ФИО")
    phone_number = models.TextField("Номер телефона")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"