from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from core.models import BaseModel

"""
Debido a que Django utiliza el campo is_active para gestionar si un usuario esta
habilitado o no para autenticarse, decidi agregar un campo is_deleted para gestionar
el borrado logico exclusivamente para este modelo, con lo cual agrego un manager
personalizado que aplique por defecto el filter y sobreescribo delete() para que
ejecute el borrado logico.
"""

class ActiveUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Country(BaseModel):
    name = models.CharField(max_length=100, verbose_name="País")

    class Meta:
        verbose_name = "País"
        verbose_name_plural = "Países"

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
    is_deleted = models.BooleanField(default=False, verbose_name="Eliminado")

    objects = ActiveUserManager()
    all_objects = UserManager()

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.is_deleted = True
        self.save(update_fields=['is_active','is_deleted','updated_at'])

    def restore(self):
            self.is_active = True
            self.is_deleted = False
            self.save(update_fields=['is_active', 'is_deleted', 'updated_at'])

    def __str__(self):
        return self.username