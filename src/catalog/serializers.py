from rest_framework import serializers
from .models import Genre, Author, Publisher, Book
from users.summary_serializers import CountrySummarySerializer
from reviews.serializers import BookReviewSummarySerializer
from .summary_serializers import (
    BookSummarySerializer,
    AuthorSummarySerializer,
    PublisherSummarySerializer,
    GenreSummarySerializer
    )

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = [
            'id',
            'name',
            'description'
        ]
        read_only_fields = fields

class PublisherSerializer(serializers.ModelSerializer):

    country = CountrySummarySerializer(read_only=True)

    class Meta:
        model = Publisher
        fields = [
            'id',
            'name',
            'country'
        ]
        read_only_fields = fields

class PublisherDetailSerializer(serializers.ModelSerializer):

    country = CountrySummarySerializer(read_only=True)
    books = BookSummarySerializer(read_only=True)

    class Meta:
        model = Publisher
        fields = [
            'id',
            'name',
            'website',
            'country',
            'books'
        ]
        read_only_fields = fields


class BookListSerializer(serializers.ModelSerializer):

    authors = AuthorSummarySerializer(many=True, read_only=True)
    publisher = PublisherSummarySerializer(read_only=True)
    genres = GenreSummarySerializer(many=True, read_only=True)
    reviews = BookReviewSummarySerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'authors',
            'publisher',
            'genres',
            'reviews',
            'publication_date',
            'cover'
        ]

class BookDetailSerializer(serializers.ModelSerializer):

    authors = AuthorSummarySerializer(many=True, read_only=True)
    publisher = PublisherSummarySerializer(read_only=True)
    genres = GenreSummarySerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'synopsis',
            'authors',
            'publisher',
            'isbn',
            'cover',
            'publication_date',
            'genres',
        ]

class AuthorSerializer(serializers.ModelSerializer):

    country = CountrySummarySerializer(read_only=True)
    class Meta:
        model = Author
        fields = [
            'id',
            'name',
            'country',
        ]
        read_only_fields = fields

class AuthorDetailSerializer(serializers.ModelSerializer):

    country = CountrySummarySerializer(read_only=True)
    books = BookSummarySerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = [
            'id',
            'name',
            'bio',
            'birth_date',
            'country',
            'books'
        ]
        read_only_fields = fields
