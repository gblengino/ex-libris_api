from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GenreViewSet, AuthorViewSet, PublisherViewSet, BookViewSet

router = DefaultRouter()

router.register("genres", GenreViewSet, basename="genres_vs")
router.register("authors", AuthorViewSet, basename="authors_vs")
router.register("publishers", PublisherViewSet, basename="publishers_vs")
router.register("books", BookViewSet, basename="books_vs")

urlpatterns = [
    path("", include(router.urls))
]