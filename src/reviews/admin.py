from django.contrib import admin
from django.db.models import Count
from .models import Review, Comment, ReadingList

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'title', 'rating', 'user', 'likes_count', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('user__username', 'book__title',)
    date_hierarchy = ('created_at')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            likes_count=Count('likes')
        )

    @admin.display(description='Likes', ordering='likes_count')
    def likes_count(self, obj):
        return obj.likes.count()

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('review__title', 'user', 'content', 'likes_count', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('content',)
    date_hierarchy = ('created_at')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            likes_count=Count('likes')
        )

    @admin.display(description='Likes', ordering='likes_count')
    def likes_count(self, obj):
        return obj.likes.count()

@admin.register(ReadingList)
class ReadingListAdmin(admin.ModelAdmin):
    list_display = ('user__username', 'book__title', 'status')
    list_filter = ('status',)
    search_fields = ('user__username', 'book__title')
    list_select_related = ('user', 'book')
    ordering = ('user__username',)