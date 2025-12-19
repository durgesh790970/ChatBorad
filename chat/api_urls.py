"""
API URL configuration for chat app.
"""
from django.urls import path
from .api_views import (
    UserListAPIView,
    ChatHistoryAPIView,
    SendMessageAPIView,
    SendFileMessageAPIView,
    OnlineStatusAPIView,
    DeleteMessageAPIView,
    MarkMessageAsReadAPIView,
    DashboardDataAPIView,
)

urlpatterns = [
    # Users API
    path('users/', UserListAPIView.as_view(), name='api_users_list'),

    # Messages API
    path('messages/history/', ChatHistoryAPIView.as_view(), name='api_chat_history'),
    path('messages/send/', SendMessageAPIView.as_view(), name='api_send_message'),
    path('messages/send-with-file/', SendFileMessageAPIView.as_view(), name='api_send_file_message'),
    path('messages/<str:id>/', DeleteMessageAPIView.as_view(), name='api_delete_message'),
    path('messages/<str:id>/mark-read/', MarkMessageAsReadAPIView.as_view(), name='api_mark_read'),

    # Online Status API
    path('status/', OnlineStatusAPIView.as_view(), name='api_online_status'),
    
    # Dashboard API
    path('dashboard/', DashboardDataAPIView.as_view(), name='api_dashboard'),
]
