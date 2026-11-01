from django.db.models import Count, Exists, OuterRef, Value, BooleanField
from .models import LikeComment, LikeReview

def with_like_data(queryset, like_model, related_field, user):
    likes = like_model.objects.filter(
        **{related_field: OuterRef('pk')}
    )

    if user and user.is_authenticated:
        likes = likes.filter(user=user)
        is_liked = Exists(likes)
    else:
        is_liked = Value(False, output_field=BooleanField())

    return queryset.annotate(
        likes_count=Count('likes', distinct=True),
        is_liked=is_liked
    )

def reviews_with_like_data(queryset, user):
    return with_like_data(
        queryset,
        LikeReview,
        'review',
        user
    )

def comments_with_like_data(queryset, user):
    return with_like_data(
        queryset,
        LikeComment,
        'comment',
        user
    )