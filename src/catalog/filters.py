import django_filters
from .models import Book, Genre
'''
Usar la clase FilterSet permite "esconder" en las peticiones como está estructurada
la base de datos. En lugar de que la url muestre 'genre__name' haciendo referencia
al campo de la tabla puedo definir un field_name específico, en este ejemplo es
solo 'genre'. De paso las queries quedan más limpias en la URL

Antes: /api/catalog/books?genres__name=1&author__name=Tolkien
Ahora: /api/catalog/books?genre=1&author=Tolkien
'''

class BookFilter(django_filters.FilterSet):

    # Genero recibe solo el id
    genre = django_filters.ModelChoiceFilter(
        field_name='genres',
        queryset=Genre.objects.all()
    )

    # Autor y publisher funcionan como busqueda search con icontains
    author = django_filters.CharFilter(
        field_name='authors__name',
        lookup_expr='icontains'
    )
    publisher = django_filters.CharFilter(
        field_name='publisher__name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Book
        fields = []