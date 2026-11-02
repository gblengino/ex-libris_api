from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter

from django.db.models import Prefetch, Count, Exists, OuterRef, Value, BooleanField
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Genre, Author, Publisher, Book
from reviews.models import Review, ReadingList
from .serializers import (
    GenreSerializer,
    AuthorSerializer,
    AuthorDetailSerializer,
    PublisherSerializer,
    PublisherDetailSerializer,
    BookListSerializer,
    BookDetailSerializer
)
from reviews.querysets import reviews_with_like_data
from .filters import BookFilter

@extend_schema(
    auth=[],
    summary='Obtener Géneros',
    description='Este endpoint devuelve la lista completa de géneros que pueden asignarse' \
    'a los libros.'
)
class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all().order_by('name', 'id')
    serializer_class = GenreSerializer

@extend_schema_view(
    list=extend_schema(
        summary = 'Listar Autores',
        description = 'Retorna una lista de autores paginada. Soporta búsqueda por nombre y ' \
        'ordenación por id y nombre (alfabético).'
    ),
    retrieve=extend_schema(
        summary = 'Obtener detalle de Autor/a',
        description = 'Retorna información detallada de un autor, así como una lista de sus ' \
        'obras anidada.'
    )
)
@extend_schema(auth=[])
class AuthorViewSet(viewsets.ReadOnlyModelViewSet):

    filter_backends = [SearchFilter, OrderingFilter]

    search_fields = ['name']
    ordering_fields = ['id','name']

    def get_queryset(self):
        queryset = Author.objects.all().order_by('name', 'id')
        if self.action == 'retrieve':
            queryset = Author.objects.all().prefetch_related('books')
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AuthorDetailSerializer
        return AuthorSerializer

@extend_schema_view(
    list=extend_schema(
        summary = 'Listar Editoriales',
        description = 'Retorna una lista de editoriales paginada. Soporta búsqueda por nombre y ' \
        'ordenación por id y nombre (alfabético).'
    ),
    retrieve=extend_schema(
        summary = 'Obtener detalle de Editorial',
        description = 'Retorna información detallada de una editorial, así como una lista de sus ' \
        'obras editadas anidada.'
    )
)
@extend_schema(auth=[])
class PublisherViewSet(viewsets.ReadOnlyModelViewSet):

    filter_backends = [SearchFilter, OrderingFilter]

    sarch_fields = ['name']
    ordering_fields = ['id', 'name']

    def get_queryset(self):
        queryset = Publisher.objects.all().order_by('name', 'id')
        if self.action == 'retrieve':
            queryset = Publisher.objects.all().prefetch_related('books')
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PublisherDetailSerializer
        return PublisherSerializer

@extend_schema_view(
    list=extend_schema(
        summary = 'Listar Libros',
        description = 'Retorna una lista de libros paginada. Soporta búsqueda por título y una serie de ' \
        'filtros: Género (ID), Autor (coincidencia parcial del nombre) y Editorial (coincidencia parcial ' \
        'del nombre). Ordenación por título (alfabético) o fecha de publicación. ' \
        'Si se envía información de un usuario autenticado, devuelve si este tiene guardado el libro en su lista.'
    ),
    retrieve=extend_schema(
        summary = 'Obtener detalle de un Libro',
        description = 'Retorna información detallada de un libro, incluyendo información anidada de sus ' \
        'autores, editorial, géneros y reseñas recientes. ' \
        'Si se envía información de un usuario autenticado, devuelve si este tiene guardado el libro en su lista.'
    )
)
class BookViewSet(viewsets.ReadOnlyModelViewSet):

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title']
    ordering_fields = ['title', 'publication_date', 'id']

    def get_queryset(self):
        
        queryset = Book.objects.all().select_related('publisher').prefetch_related('authors', 'genres').order_by('title', 'id')

        if self.request.user.is_authenticated:
            user_reading_list = ReadingList.objects.filter(
                user=self.request.user,
                book=OuterRef('pk')
            )
            queryset = queryset.annotate(
                is_in_reading_list = Exists(user_reading_list)
            )
        else:
            queryset = queryset.annotate(
                is_in_reading_list = Value(False, output_field=BooleanField())
            )
        
        if self.action == 'retrieve':

            # El detail de los libros trae solamente las ultimas 5 reseñas, para ver
            # todas las reseñas se debe seleccionar el libro correspondiente desde
            # el endpoint de reviews con el filter que corresponde.
            latest_reviews = reviews_with_like_data(
                Review.objects.order_by('-created_at','-id')[:5],
                self.request.user
            )

            queryset = queryset.prefetch_related(
                Prefetch(
                    'reviews',
                    queryset=latest_reviews,
                    to_attr='latest_reviews'
                )
            )

        queryset = queryset.annotate(
            reviews_count=Count('reviews', distinct=True)
        )

        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BookDetailSerializer
        return BookListSerializer
