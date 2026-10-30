from django.contrib.auth.models import AbstractUser
from django.db import models
from core.models import BaseModel

class Country(BaseModel):
    name = models.CharField(max_length=100, verbose_name="País")

    def __str__(self):
        return self.name

class CustomUser(AbstractUser, BaseModel):
    bio = models.TextField(blank=True, null=True, verbose_name="Biografía")
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios',
        verbose_name="País"
    )

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.username