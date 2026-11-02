from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from django.db.models import Prefetch, Count

from django_filters.rest_framework import DjangoFilterBackend

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

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['book']

    # Consulta optimizada
    def get_queryset(self):
        # Trae usuario y libro para el nested
        queryset = Review.objects.select_related(
            'user',
            'book',
        )
        
        if self.action == 'retrieve':

            latest_comments = comments_with_like_data(
                Comment.objects.select_related('user').order_by(
                    '-created_at',
                    '-id'
                ),
                self.request.user
            )[:10]

            # Si es un retrieve, prefetchea los comentarios
            queryset = queryset.prefetch_related(
                Prefetch(
                    'comments',
                    queryset=latest_comments,
                    to_attr='latest_comments'
                )
            )

        if self.action == 'list':
            queryset = queryset.annotate(
                comments_count=Count('comments', distinct=True)
            )

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

        like, created = LikeReview.objects.get_or_create(
            user = request.user,
            review = review
        )
        if created:
            return Response(status=status.HTTP_201_CREATED)

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

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review']

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

        like, created = LikeComment.objects.get_or_create(
            user = request.user,
            comment = comment
        )
        if created:
            return Response(status=status.HTTP_201_CREATED)

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