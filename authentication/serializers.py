from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'pk',
            'email',
            'is_staff',
            'is_superuser',
            'password',
            'is_active'
        ]
