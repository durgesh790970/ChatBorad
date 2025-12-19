"""
Django REST Framework serializers for chat app.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Message, UserProfile


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    is_online = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_online']

    def get_is_online(self, obj):
        """Get online status from user profile"""
        try:
            return obj.profile.is_online
        except:
            return False


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model"""
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    receiver_username = serializers.CharField(source='receiver.username', read_only=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'sender',
            'sender_username',
            'receiver',
            'receiver_username',
            'message_text',
            'timestamp',
            'is_read'
        ]
        read_only_fields = ['id', 'timestamp', 'sender_username', 'receiver_username']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model"""
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'is_online', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
