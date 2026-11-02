from django.contrib import admin
from .models import Genre, Author, Publisher, Book

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name','birth_date', 'country', 'is_active', 'created_at', 'updated_at')
    list_filter = ('country', 'is_active')
    search_fields = ('name',)

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'country', 'is_active', 'created_at', 'updated_at')
    list_filter = ('country', 'is_active')
    search_fields = ('name', 'website',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_authors', 'publisher', 'publication_date', 'is_active')
    list_filter = ('genres', 'is_active')
    search_fields = ('title', 'authors', 'publisher', 'genres')

    @admin.display(description="Autores")
    def get_authors(self, obj):
        return ', '.join(author.name for author in obj.authors.all())