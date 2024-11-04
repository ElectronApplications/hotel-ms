from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Client(models.Model):
    name = models.TextField("ФИО")
    phone_number = models.CharField(
        "Номер телефона",
        max_length=16,
        unique=True,
        validators=[
            RegexValidator(r"^[+][\d]{7,15}$")
        ]
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    class Role(models.TextChoices):
        CLIENT = "client", "Клиент"
        RECEPTION = "reception", "Ресепшен"
        SERVICE = "service", "Обслуживание"
        CLEANING = "cleaning", "Уборка"
        PLANNING = "planning", "Планировка"
        ADMIN = "admin", "Администрирование"
    role = models.CharField(max_length=16, choices=Role.choices, default=Role.CLIENT)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"