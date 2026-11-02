from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from django.db.models import Prefetch, Count

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Review, Comment, ReadingList, LikeComment, LikeReview
from .serializers import (
    ReviewListSerializer,
    ReviewDetailSerializer,
    ReviewCreateSerializer,
    ReviewUpdateSerializer,
    CommentSerializer,
    CommentCreateSerializer,
    CommentUpdateSerializer,
    ReadingListSerializer,
    ReadingListCreateSerializer,
    ReadingListUpdateSerializer,
)
from .permissions import IsAuthorOrReadOnly
from .querysets import reviews_with_like_data, comments_with_like_data

@extend_schema_view(
    list=extend_schema(
        summary = 'Listar Reseñas',
        description = (
            'Retorna una lista paginada de reseñas. <br>'
            '<br>'
            '**Filtros:** <br>'
            '- Por libro (ID). <br>'
            '<br>'
            '**Información adicional:** <br>'
            '- Devuelve la lista de reseñas **ordenada por las más recientes**'
            '- Indica si el usuario autenticado dio like a la reseña. Si no se proporciona un token de autenticación, devuelve `false` por defecto.<br>'
            '<br>'
            '**Recomendaciones:**<br>'
            'Se recomienda utilizar este endpoint **exclusivamente** filtrando por libro para listar todas las reseñas de un libro.'
        )
    ),
    retrieve=extend_schema(
        summary = 'Obtener detalle de Reseña',
        description = (
            'Retorna información detallada de una Reseña. <br>'
            '<br>'
            '**Información adicional:** <br>'
            '- Trae anidados los últimos 10 comentarios realizados.<br>'
            '- Trae la cantidad de likes que tiene la reseña.<br>'
            '- Indica si el usuario autenticado dio like a la reseña. Si no se proporciona un token de autenticación, devuelve `false` por defecto.<br>'
            '<br>'
            '**Recomendaciones:**<br>'
            'Se recomienda utilizar el endpoint **/comments** con la query filtrada por la review para traer la lista completa y paginada de comentarios.'
        )
    ),
    create=extend_schema(
        summary = 'Crear Reseña',
        description = (
            'Permite crear una nueva reseña de un libro. Requiere del ID del libro. <br>'
            'La información del usuario se envía mediante el token JWT, no se requiere ' \
            'enviar el ID del usuario.'
        )
    ),
    update=extend_schema(
        summary = 'Actualizar Reseña',
        description = 'Permite actualizar una reseña. El usuario solo puede editar reseñas de ' \
        'su autoría.'
    ),
    partial_update=extend_schema(
        summary = 'Actualizar Reseña',
        description = 'Permite actualizar una reseña. El usuario solo puede editar reseñas de ' \
        'su autoría.'
    ),
    destroy=extend_schema(
        summary = 'Eliminar Reseña',
        description = 'Elimina la reseña de la autoría del usuario autenticado.'
    )
)
class ReviewViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['book']

    # Consulta optimizada
    def get_queryset(self):
        # Trae usuario y libro para el nested
        queryset = Review.objects.select_related(
            'user',
            'book',
        )
        
        if self.action == 'retrieve':

            latest_comments = comments_with_like_data(
                Comment.objects.select_related('user').order_by(
                    '-created_at',
                    '-id'
                ),
                self.request.user
            )[:10]

            # Si es un retrieve, prefetchea los comentarios
            queryset = queryset.prefetch_related(
                Prefetch(
                    'comments',
                    queryset=latest_comments,
                    to_attr='latest_comments'
                )
            )

        if self.action == 'list':
            queryset = queryset.annotate(
                comments_count=Count('comments', distinct=True)
            )

        # Usa la funcion de querysets.py para calcular la
        # cantidad de likes que tiene la review
        queryset = reviews_with_like_data(
            queryset,
            self.request.user
        )

        # Devuelve la lista ordenada por la mas reciente
        return queryset.order_by('-created_at', '-id')

    def get_serializer_class(self):

        if self.action == 'retrieve':
            return ReviewDetailSerializer

        if self.action == 'create':
            return ReviewCreateSerializer

        if self.action in ['update', 'partial_update']:
            return ReviewUpdateSerializer

        return ReviewListSerializer

    # Redefine create para pasarle el usuario del request, asi evito
    # enviar el id del usuario en el JSON y que puedan crear una review
    # de otro usuario.
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # --- ACCIONES PERSONALIZADAS: LIKES ---

    # Dar like
    @extend_schema(
            summary='Likear Reseña',
            description='El usuario da like a la reseña. No requiere body',
            request=None,
            responses={201: None, 204: None}
    )
    @action(detail=True, methods=['post'],permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        review = self.get_object()

        like, created = LikeReview.objects.get_or_create(
            user = request.user,
            review = review
        )
        if created:
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
            summary='Quitar Like Reseña',
            description='El usuario quita su like a una reseña. No requiere body',
            request=None,
            responses={204: None}
    )
    @action(detail=True, methods=['delete'],permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):

        review = self.get_object()

        LikeReview.objects.filter(
            user=request.user,
            review=review
        ).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema_view(
    list=extend_schema(
        summary = 'Listar Comentarios',
        description = (
            'Retorna una lista paginada de comentarios. <br>'
            '<br>'
            '**Filtros:** <br>'
            '- Por reseña (ID). <br>'
            '<br>'
            '**Información adicional:** <br>'
            '- Devuelve la lista de comentarios **ordenada por los más recientes**<br>'
            '- Indica si el usuario autenticado dio like al comentario. Si no se proporciona un token de autenticación, devuelve `false` por defecto.<br>'
            '<br>'
            '**Recomendaciones:**<br>'
            'Se recomienda utilizar este endpoint **exclusivamente** filtrando por reseña para listar todos los comentarios de una reseña.'
        )
    ),
    retrieve=extend_schema(
        summary = 'Obtener detalle de Comentario',
        description = (
            'Retorna la misma información que un comentario de una lista.<br>'
        )
    ),
    create=extend_schema(
        summary = 'Crear Comentario',
        description = (
            'Permite crear un nuevo comentario para una reseña. Requiere del ID de la reseña. <br>'
            'La información del usuario se envía mediante el token JWT, no se requiere ' \
            'enviar el ID del usuario.'
        )
    ),
    update=extend_schema(
        summary = 'Actualizar Comentario',
        description = 'Permite actualizar un comentario. El usuario solo puede editar comentarios de ' \
        'su autoría.'
    ),
    partial_update=extend_schema(
        summary = 'Actualizar Comentario',
        description = 'Permite actualizar un comentario. El usuario solo puede editar comentarios de ' \
        'su autoría.'
    ),
    destroy=extend_schema(
        summary = 'Eliminar Comentario',
        description = 'Elimina el comentario de la autoría del usuario autenticado.'
    )
)
class CommentViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review']

    def get_queryset(self):

        queryset = Comment.objects.select_related('user')

        queryset = comments_with_like_data(
            queryset,
            self.request.user
        )

        return queryset.order_by('-created_at','-id')

    def get_serializer_class(self):

        if self.action == 'create':
            return CommentCreateSerializer

        if self.action in ['update', 'partial_update']:
            return CommentUpdateSerializer

        return CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # --- ACCIONES PERSONALIZADAS: LIKES ---
    
    @extend_schema(
            summary='Likear Comentario',
            description='El usuario da like al comentario. No requiere body',
            request=None,
            responses={201: None, 204: None}
    )
    @action(detail=True, methods=['post'],permission_classes=[IsAuthenticated])

    def like(self, request, pk=None):
        comment = self.get_object()

        like, created = LikeComment.objects.get_or_create(
            user = request.user,
            comment = comment
        )
        if created:
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
            summary='Quitar Like Comentario',
            description='El usuario quita su like a un comentario. No requiere body',
            request=None,
            responses={204: None}
    )
    @action(detail=True, methods=['delete'],permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):

        comment = self.get_object()

        LikeComment.objects.filter(
            user=request.user,
            comment=comment
        ).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema_view(
    list=extend_schema(
        summary = 'Listar Lecturas',
        description = (
            'Retorna una lista paginada de los libros + estado de lectura del usuario autenticado.<br>'
            'Solo funciona si recibe un Token de Autenticación ya que utiliza la información del usuario ' \
            'que provee el token para traer su Lista de Lecturas.'
        )
    ),
    retrieve=extend_schema(
        summary = 'Obtener detalle de Lecturas',
        description = (
            'Retorna la misma información que un libro + estado de la lista.<br>'
        )
    ),
    create=extend_schema(
        summary = 'Añadir Lectura',
        description = (
            'Añade el libro enviado en el body a la lista de lectura del usuario autenticado y le agrega por' \
            'defecto el estado: `TO_READ`'
        )
    ),
    update=extend_schema(
        summary = 'Actualizar Lectura',
        description = 'Actualiza el estado de lectura de un libro. Para ello el endpoint debe recibir el id de ' \
        'la **relación** (provisto en el `GET` list de este endpoint).<br>Se realiza de esta forma para evitar ' \
        'que se edite por error el estado de otro libro, de un libro inexistente o del libro de otro usuario.'
    ),
    partial_update=extend_schema(
        summary = 'Actualizar Lectura',
            description = 'Actualiza el estado de lectura de un libro. Para ello el endpoint debe recibir el id de ' \
            'la **relación** (provisto en el `GET` list de este endpoint).<br>Se realiza de esta forma para evitar ' \
            'que se edite por error el estado de otro libro, de un libro inexistente o del libro de otro usuario.'
    ),
    destroy=extend_schema(
        summary = 'Eliminar Lectura',
        description = 'Elimina la lectura de la lista de lecturas del usuario.'
    )
)
class ReadingListViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ReadingList.objects.filter(
            user=self.request.user
        ).select_related('book').order_by('-created_at', '-id')

    def get_serializer_class(self):

        if self.action == 'create':
            return ReadingListCreateSerializer

        if self.action in ['update', 'partial_update']:
            return ReadingListUpdateSerializer

        return ReadingListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)