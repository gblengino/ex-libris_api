from rest_framework import serializers
from .models import Genre, Author, Publisher, Book
from users.models import Country

class CountrySummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']

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

class AuthorSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']

class GenreSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class PublisherSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name']

class BookSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_date']


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


class BookSerializer(serializers.ModelSerializer):

    authors = AuthorSummarySerializer(many=True, read_only=True)
    publisher = PublisherSummarySerializer(read_only=True)
    genres = GenreSummarySerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'authors',
            'publisher',
            'genres',
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
