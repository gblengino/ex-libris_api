from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema

from .serializers import RegisterSerializer, ProfileSerializer, PublicUserSerializer

User = get_user_model()

"""
La clase ProfileViewSet de estas vistas heredan ViewSet en lugar de ModelViewSet porque no necesito el CRUD
completo sino acciones especificas y que las otras directamente no esten disponibles por razones
de seguridad. De ese modo puedo mantener el uso de ViewSets y al mismo tiempo proteger las vistas.
"""

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    @extend_schema(
            summary='Registro',
            description='Registra nuevos usuarios en la plataforma.',
            auth=[],
            )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save() # Esto dispara automáticamente el método create() del serializador
        
        return Response(
            {'message': 'Usuario registrado correctamente.'},
            status=status.HTTP_201_CREATED
        )

@extend_schema(
    description='La información del usuario se envía y recibe dentro del token de autenticación JWT,' \
    'por eso no se solicita el id del usuario.'
)
class ProfileViewSet(viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Usuario obtiene su perfil',
        methods=['GET'],
        responses=ProfileSerializer
    )
    @extend_schema(
        summary='Usuario edita su perfil',
        methods=['PATCH'],
        request=ProfileSerializer,
        responses=ProfileSerializer
    )
    @action(detail=False, methods=['get', 'patch'])
    def profile(self, request):
        if request.method == 'GET':
            serializer = ProfileSerializer(request.user)
            return Response(serializer.data)

        serializer = ProfileSerializer(
            request.user,
            data=request.data,
            partial = True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='Usuario borra su perfil',
        methods=['DELETE'],
        request=None,
        responses={204: None}
    )
    @action(detail=False, methods=['delete'])
    def delete(self, request):
        user = request.user
        user.delete()
        return Response(
            {"message": "Tu cuenta ha sido borrada exitosamente."},
            status=status.HTTP_204_NO_CONTENT
        )

class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = PublicUserSerializer
    permission_classes = [AllowAny]

    @extend_schema(
            summary="Lista de Usuarios",
            description="Obtiene la lista de todos los usuarios paginada."
    )
    def list(self, request):
        queryset = self.queryset
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(serializer.data)

    @extend_schema(
            summary='Detalle de Usuario',
            description='Responde la información pública de un usuario.' \
            'Se puede usar para mostrar perfiles.'
    )
    def retrieve(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)