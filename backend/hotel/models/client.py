from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    name = models.TextField("ФИО")
    phone_number = models.TextField("Номер телефона")
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"