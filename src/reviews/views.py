from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Review, Comment, ReadingList, LikeComment, LikeReview
from .serializers import (
    ReviewListSerializer,
    ReviewDetailSerializer,
    ReviewCreateSerializer,
    ReviewUpdateSerializer,
    CommentSerializer,
    CommentCreateSerializer,
    CommentUpdateSerializer,
    ReadingListSerializer,
    ReadingListCreateSerializer,
    ReadingListUpdateSerializer,
)
from .permissions import IsAuthorOrReadOnly
from .querysets import reviews_with_like_data, comments_with_like_data

class ReviewViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    # Consulta optimizada
    def get_queryset(self):
        # Trae usuario y libro para el nested
        queryset = Review.objects.select_related(
            'user',
            'book',
        )
        
        if self.action == 'retrieve':
            # Si es un retrieve, prefetchea los comentarios
            queryset = queryset.prefetch_related('comments__user')

        # Usa la funcion de querysets.py para calcular la
        # cantidad de likes que tiene la review
        queryset = reviews_with_like_data(
            queryset,
            self.request.user
        )

        # Devuelve la lista ordenada por la mas reciente
        return queryset.order_by('-created_at', '-id')

    def get_serializer_class(self):

        if self.action == 'retrieve':
            return ReviewDetailSerializer

        if self.action == 'create':
            return ReviewCreateSerializer

        if self.action in ['update', 'partial_update']:
            return ReviewUpdateSerializer

        return ReviewListSerializer

    # Redefine create para pasarle el usuario del request, asi evito
    # enviar el id del usuario en el JSON y que puedan crear una review
    # de otro usuario.
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # --- ACCIONES PERSONALIZADAS: LIKES ---

    # Dar like
    @action(detail=True, methods=['post'],permission_classes=[IsAuthenticated])

    def like(self, request, pk=None):
        review = self.get_object()

        LikeReview.objects.get_or_create(
            user = request.user,
            review = review
        )

        return Response(status=status.HTTP_204_NO_CONTENT)

    # Quitar like
    @action(detail=True, methods=['delete'],permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):

        review = self.get_object()

        LikeReview.objects.filter(
            user=request.user,
            review=review
        ).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):

        queryset = Comment.objects.select_related('user')

        queryset = comments_with_like_data(
            queryset,
            self.request.user
        )

        return queryset.order_by('-created_at','-id')

    def get_serializer_class(self):

        if self.action == 'create':
            return CommentCreateSerializer

        if self.action in ['update', 'partial_update']:
            return CommentUpdateSerializer

        return CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # --- ACCIONES PERSONALIZADAS: LIKES ---
    
    # Dar like
    @action(detail=True, methods=['post'],permission_classes=[IsAuthenticated])

    def like(self, request, pk=None):
        comment = self.get_object()

        LikeComment.objects.get_or_create(
            user = request.user,
            comment = comment
        )

        return Response(status=status.HTTP_204_NO_CONTENT)

    # Quitar like
    @action(detail=True, methods=['delete'],permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):

        comment = self.get_object()

        LikeComment.objects.filter(
            user=request.user,
            comment=comment
        ).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class ReadingListViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ReadingList.objects.filter(
            user=self.request.user
        ).select_related('book').order_by('-created-at', '-id')

    def get_serializer_class(self):

        if self.action == 'create':
            return ReadingListCreateSerializer

        if self.action in ['update', 'partial_update']:
            return ReadingListUpdateSerializer

        return ReadingListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)