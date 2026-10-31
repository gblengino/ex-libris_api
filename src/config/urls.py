from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include([
        path('register/', RegisterView.as_view(), name='auth_register'),
        path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('refresh/', TokenRefreshView.as_view(), name='token_refresh')
    ])),
    path('api/users/', include("users.urls")),
    path('api/catalog/', include("catalog.urls"))
]