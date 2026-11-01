from rest_framework import serializers
from .models import Review, Comment, ReadingList
from users.summary_serializers import UserSummarySerializer
from catalog.serializers import BookSummarySerializer

# ---- SERIALIZERS PARA COMENTARIOS ----

class CommentSerializer(serializers.ModelSerializer):

    user = UserSummarySerializer(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.BooleanField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'content',
            'likes_count',
            'created_at'
        ]

class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        fields = [
            'review',
            'content'
        ]

# ---- SERIALIZERS PARA REVIEWS ----

class ReviewSerializer(serializers.ModelSerializer):
    
    user = UserSummarySerializer(read_only=True)
    book = BookSummarySerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'book',
            'title',
            'content',
            'rating',
            'likes_count',
            'is_liked',
            'comments',
            'created_at',
            'updated_at',
        ]

class ReviewCreateSerializer(serializers.ModelSerializer):
    # Serializer para crear reviews, el usuario se asigna desde el ViewSet
    # como medida de seguridad (su info viene mediante el auth system)
    class Meta:
        model = Review
        fields = [
            'book',
            'title',
            'content',
            'rating'
        ]

class UserReviewSummarySerializer(serializers.ModelSerializer):
    # Serializer para anidar las reviews dentro de un usuario
    book = BookSummarySerializer(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.BooleanField(read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'book',
            'title',
            'rating',
            'likes_count',
            'is_liked',
            'created_at'
        ]

class BookReviewSummarySerializer(serializers.ModelSerializer):
    # Serializer para anidar las reviews dentro de un libro
    user = UserSummarySerializer(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.BooleanField(read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'title',
            'rating',
            'likes_count',
            'is_liked',
            'created_at'
        ]

class ReadingListSerializer(serializers.ModelSerializer):

    book = BookSummarySerializer(read_only=True)

    class Meta:
        model = ReadingList
        fields = [
            'id', 'book', 'status'
        ]
        read_only_fields = fields

class ReadingListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingList
        fields = ['book']

class ReadingListUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingList
        fields = ['status']