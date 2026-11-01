from django.db import models
from core.models import BaseModel

class Review(BaseModel):

    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    book = models.ForeignKey(
        'catalog.Book',
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    title = models.CharField(max_length=150, verbose_name="Título")
    content = models.TextField(verbose_name="Contenido")
    rating = models.PositiveSmallIntegerField(verbose_name="Calificación")

    class Meta:
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'book'],
                name='unique_user_book_review'
            ),
            models.CheckConstraint(
                condition=models.Q(rating__gte=1, rating__lte=10),
                name='review_rating_range'
            )
        ]

class LikeReview(models.Model):

    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='liked_reviews'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Me gusta de reseña"
        verbose_name_plural = "Me gusta de reseñas"

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'review'],
                name='unique_user_review_like'
            )
        ]

class Comment(BaseModel):

    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    content = models.TextField(verbose_name="Comentario")

    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"

class LikeComment(models.Model):

    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='liked_comments'
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    class Meta:
        verbose_name = "Me gusta de comentario"
        verbose_name_plural = "Me gusta de comentarios"

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'comment'],
                name='unique_user_comment_like'
            )
        ]

class ReadingList(BaseModel):

    class ReadingStatus(models.TextChoices):
        TO_READ = 'TO_READ', 'Por leer'
        READING = 'READING', 'Leyendo'
        FINISHED = 'FINISHED', 'Terminado'
        ABANDONED = 'ABANDONED', 'Abandonado'

    user = models.ForeignKey(
            'users.CustomUser',
            on_delete=models.CASCADE,
            related_name='reading_list'
        )
    book = models.ForeignKey(
        'catalog.Book',
        on_delete=models.CASCADE,
        related_name='reading_lists'
    )

    status = models.CharField(
        max_length=10,
        choices=ReadingStatus.choices,
        default=ReadingStatus.TO_READ
    )

    class Meta:
        verbose_name = "Lista de lectura"
        verbose_name_plural = "Listas de lectura"

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'book'],
                name='unique_user_reading_list_book_'
            )
        ]
