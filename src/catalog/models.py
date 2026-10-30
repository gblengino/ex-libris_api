from django.db import models
from core.models import BaseModel

class Genre(BaseModel):
    name = models.CharField(max_length=50, verbose_name="Género")
    description = models.TextField(blank=True, verbose_name="Descripción")

    class Meta:
        verbose_name = "Género"
        verbose_name_plural = "Géneros"

    def __str__(self):
        return self.name

class Publisher(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Editorial")
    website = models.URLField(
        max_length=200,
        blank=True,
        verbose_name="Sitio web"
        )
    country = models.ForeignKey(
        'users.Country',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='publishers',
        verbose_name="País"
    )

    def __str__(self):
        return self.name

class Author(BaseModel):
    name = models.CharField(max_length=150, verbose_name="Nombre")
    bio = models.TextField(verbose_name="Biografía (reseña)")
    birth_date = models.DateField(verbose_name="Fecha de Nacimiento")
    country = models.ForeignKey(
        'users.Country',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='authors',
        verbose_name="Nacionalidad"
    )

    def __str__(self):
        return self.name

class Book(BaseModel):
    title = models.CharField(max_length=200, verbose_name="Título")
    synopsis = models.TextField(verbose_name="Sinopsis")
    publication_date = models.DateField(verbose_name="Fecha de Publicación")
    isbn = models.CharField(max_length=13, verbose_name="ISBN")
    cover = models.ImageField(
        upload_to='books/covers/',
        blank=True,
        null=True,
        verbose_name="Portada"
    )
    authors = models.ManyToManyField(
        Author,
        related_name='books'
    )
    genres = models.ManyToManyField(
        Genre,
        related_name='books'
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.PROTECT,
        related_name='books'
    )

    def __str__(self):
        return self.title