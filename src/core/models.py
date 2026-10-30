from django.db import models

class ActiveManager(models.Manager):
    # Clase para reemplazar el Manager que usa Django para las consultas SQL
    def get_queryset(self):
        # Reescritura del QuerySet para que filtre por el campo de borrado logico
        return super().get_queryset().filter(is_active=True)

class BaseModel(models.Model):
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última modificación")

    objects = ActiveManager()       # Usa por defecto el ActiveManager declarado arriba
    all_objects = models.Manager()  # Declaro un manager secundario que devuelva todos los registros

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        # Reemplazo del metodo delete() para ejecutar un borrado logico
        self.is_active = False
        self.save(update_fields=['is_active', 'updated_at'])

    def restore(self):
        # Metodo restore() para restaurar datos borrados logicamente
        self.is_active = True
        self.save(update_fields=['is_active', 'updated_at'])