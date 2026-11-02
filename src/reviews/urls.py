from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, CommentViewSet

router = DefaultRouter()

router.register(r"reviews", ReviewViewSet, basename="reviews_vs")
router.register(r"comments", CommentViewSet, basename="comments_vs")

urlpatterns = [
    path("", include(router.urls))
]