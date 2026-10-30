from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save() # Esto dispara automáticamente el método create() del serializador
        
        return Response(
            {'message': 'Usuario registrado correctamente.'},
            status=status.HTTP_201_CREATED
        )

    # Creacion de usuario
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data.copy()
        data.pop('password2', None) # Elimina la confirmacion de contraseña

        password = data.pop('password')

        user = User(**data)
        # set_password() hashea la contraseña
        user.set_password(password)
        user.save()

        return Response(
            {'message': 'Usuario registrado correctamente.'},
            status=status.HTTP_201_CREATED
        )

class ProfileViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    # Action especifico para 
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

    def list(self, request):
        queryset = self.queryset
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)