from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter

from django.db.models import Prefetch, Count, Exists, OuterRef, Value, BooleanField
from django_filters.rest_framework import DjangoFilterBackend

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

class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all().order_by('name', 'id')
    serializer_class = GenreSerializer

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
