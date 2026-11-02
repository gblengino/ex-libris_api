from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from users.views import RegisterView
from reviews.views import ReadingListViewSet

# Lo declare aqui simplemente para mantener limpia la api, la lista de lectura
# deberia tener su propio endpoint y no estar englobada en /reviews/
readinglist_router = DefaultRouter()
readinglist_router.register(r'', ReadingListViewSet, basename="readinglist")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include([
        path('register/', RegisterView.as_view(), name='auth_register'),
        path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('logout/', TokenBlacklistView.as_view(), name='token_blacklist')
    ])),
    path('api/users/', include("users.urls")),
    path('api/catalog/', include("catalog.urls")),
    path('api/', include("reviews.urls")),
    path('api/readinglist/', include(readinglist_router.urls)),
]