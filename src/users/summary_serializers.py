from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Country


User = get_user_model()

class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username'
        ]
        read_only_fields = fields

class CountrySummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']