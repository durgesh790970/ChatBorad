"""
Django REST Framework API views for chat app.
"""
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Message, UserProfile
from .serializers import UserSerializer, MessageSerializer


class UserListAPIView(generics.ListAPIView):
    """
    API endpoint to list all users except the current user.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return all users except the current user
        return User.objects.exclude(id=self.request.user.id)


class ChatHistoryAPIView(generics.ListAPIView):
    """
    API endpoint to fetch chat history between two users.
    Query Parameters:
        - other_user_id: ID of the other user in the conversation
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        other_user_id = self.request.query_params.get('other_user_id')

        if not other_user_id:
            return Message.objects.none()

        try:
            other_user = User.objects.get(id=other_user_id)
        except User.DoesNotExist:
            return Message.objects.none()

        # Fetch messages between current user and other user
        messages = Message.objects.filter(
            Q(sender=current_user, receiver=other_user) |
            Q(sender=other_user, receiver=current_user)
        ).order_by('timestamp')

        # Mark received messages as read
        received_messages = messages.filter(
            sender=other_user,
            receiver=current_user,
            is_read=False
        )
        received_messages.update(is_read=True)

        return messages


class SendMessageAPIView(generics.CreateAPIView):
    """
    API endpoint to send a message.
    POST body:
        - receiver_id: ID of the receiver
        - message_text: The message content
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        receiver_id = request.data.get('receiver_id')
        message_text = request.data.get('message_text', '').strip()

        if not receiver_id or not message_text:
            return Response(
                {'error': 'receiver_id and message_text are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'Receiver not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if receiver == request.user:
            return Response(
                {'error': 'You cannot send message to yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create message
        message = Message.objects.create(
            sender=request.user,
            receiver=receiver,
            message_text=message_text
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OnlineStatusAPIView(generics.UpdateAPIView):
    """
    API endpoint to update user's online status.
    PATCH body:
        - is_online: boolean value
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        is_online = request.data.get('is_online')

        if is_online is None:
            return Response(
                {'error': 'is_online field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            profile = request.user.profile
            profile.is_online = bool(is_online)
            profile.save()

            return Response({
                'username': request.user.username,
                'is_online': profile.is_online,
                'message': 'Online status updated successfully.'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DeleteMessageAPIView(generics.DestroyAPIView):
    """
    API endpoint to delete a message.
    DELETE /api/messages/{message_id}/
    Only the sender can delete their own message.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        try:
            message = self.get_object()
            
            # Only allow sender to delete their own message
            if message.sender != request.user:
                return Response(
                    {'error': 'You can only delete your own messages.'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            message_id = message.id
            message.delete()
            
            return Response({
                'success': True,
                'message_id': str(message_id),
                'message': 'Message deleted successfully.'
            }, status=status.HTTP_200_OK)
            
        except Message.DoesNotExist:
            return Response(
                {'error': 'Message not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MarkMessageAsReadAPIView(generics.UpdateAPIView):
    """
    API endpoint to mark a message as read.
    PATCH /api/messages/{message_id}/mark-read/
    """
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        try:
            message = self.get_object()
            
            # Only receiver can mark as read
            if message.receiver != request.user:
                return Response(
                    {'error': 'You can only mark your received messages as read.'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Mark as read
            message.read_message()
            
            return Response({
                'success': True,
                'message_id': str(message.id),
                'is_read': True,
                'read_at': message.read_at.isoformat() if message.read_at else None
            }, status=status.HTTP_200_OK)
            
        except Message.DoesNotExist:
            return Response(
                {'error': 'Message not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SendFileMessageAPIView(generics.CreateAPIView):
    """
    API endpoint to send a message with file attachment.
    POST body (multipart):
        - message: Message text (optional)
        - file: File to upload
        - other_user_id: ID of the receiver
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        other_user_id = request.POST.get('other_user_id')
        message_text = request.POST.get('message', '').strip()
        uploaded_file = request.FILES.get('file')

        if not other_user_id:
            return Response(
                {'error': 'other_user_id is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not uploaded_file and not message_text:
            return Response(
                {'error': 'Either message or file is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            other_user = User.objects.get(id=other_user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'Receiver not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if other_user == request.user:
            return Response(
                {'error': 'You cannot send message to yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Create message
            message = Message.objects.create(
                sender=request.user,
                receiver=other_user,
                message_text=message_text
            )

            # Attach file if provided
            if uploaded_file:
                message.file_attachment = uploaded_file
                message.file_name = uploaded_file.name
                message.file_type = uploaded_file.content_type
                message.save()

            serializer = self.get_serializer(message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DashboardDataAPIView(generics.ListAPIView):
    """
    API endpoint to get dashboard data with sorted contacts and unread counts.
    Returns contacts sorted by latest message (most recent first).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        from django.db import models as django_models
        
        current_user = request.user
        all_users = User.objects.exclude(id=current_user.id)
        
        # Get unread count and latest message for each user
        user_data = []
        for user in all_users:
            unread_count = Message.objects.filter(
                sender=user,
                receiver=current_user,
                is_read=False
            ).count()
            
            # Get latest message timestamp with this user (sent or received)
            latest_message = Message.objects.filter(
                Q(sender=current_user, receiver=user) |
                Q(sender=user, receiver=current_user)
            ).order_by('-timestamp').first()
            
            latest_timestamp = latest_message.timestamp.isoformat() if latest_message else None
            
            user_data.append({
                'id': user.id,
                'username': user.username,
                'full_name': user.get_full_name() or user.username,
                'is_online': user.profile.is_online if hasattr(user, 'profile') else False,
                'unread_count': unread_count,
                'latest_timestamp': latest_timestamp
            })
        
        # Sort by latest message (most recent first)
        user_data.sort(key=lambda x: x['latest_timestamp'] or '', reverse=True)
        
        return Response({
            'success': True,
            'users': user_data
        }, status=status.HTTP_200_OK)
