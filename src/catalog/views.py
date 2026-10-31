from rest_framework import viewsets
from .models import Genre, Author, Publisher, Book
from .serializers import (
    GenreSerializer,
    AuthorSerializer,
    AuthorDetailSerializer,
    PublisherSerializer,
    PublisherDetailSerializer,
    BookSerializer,
    BookDetailSerializer
)

class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all().order_by('name', 'id')
    serializer_class = GenreSerializer

class AuthorViewSet(viewsets.ReadOnlyModelViewSet):

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
    queryset = Book.objects.all().select_related('publisher').prefetch_related('authors', 'genres').order_by('title', 'id')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BookDetailSerializer
        return BookSerializer
