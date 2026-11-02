from rest_framework import serializers
from .models import Review, Comment, ReadingList
from users.summary_serializers import UserSummarySerializer
from catalog.summary_serializers import BookSummarySerializer

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
            'is_liked',
            'created_at'
        ]

class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = [
            'review',
            'content'
        ]

class CommentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['content']

# ---- SERIALIZERS PARA REVIEWS ----

class ReviewListSerializer(serializers.ModelSerializer):
    
    user = UserSummarySerializer(read_only=True)
    book = BookSummarySerializer(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'book',
            'title',
            'rating',
            'likes_count',
            'is_liked',
            'created_at',
            'updated_at',
        ]

class ReviewDetailSerializer(ReviewListSerializer):

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
            'comments',
            'likes_count',
            'is_liked',
            'created_at',
            'updated_at',
        ]

class ReviewCreateSerializer(serializers.ModelSerializer):
    # Serializer para crear reviews, el usuario se asigna desde el ViewSet
    # como medida de seguridad (su info viene mediante el auth system)

    rating = serializers.IntegerField(min_value=1,max_value=10)

    class Meta:
        model = Review
        fields = [
            'book',
            'title',
            'content',
            'rating'
        ]

class ReviewUpdateSerializer(serializers.ModelSerializer):
    # Serializer para modificar aparte para impedir que un usuario pueda
    # cambiar el libro al cual le hace la reseña.
    rating = serializers.IntegerField(min_value=1,max_value=10)
    
    class Meta:
        model = Review
        fields = [
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

    def validate_book(self, value):
        user = self.context['request'].user

        if ReadingList.objects.filter(user=user, book=value).exists():
            raise serializers.ValidationError(
                'Este libro ya se encuentra en tu lista de lectura.'
            )
        return value

class ReadingListUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ReadingList
        fields = ['status']