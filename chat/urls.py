"""
URL configuration for chat app views.
"""
from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # Authentication URLs
    path('', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Chat URLs
    path('chat/<int:user_id>/', views.chat_view, name='chat'),
    path('ai-chat/', views.ai_chat_view, name='ai_chat'),
    
    # Online Status URLs
    path('online-status/', views.online_status_view, name='online_status'),
    
    # API URLs
    path('api/online-status/', views.api_online_status, name='api_online_status'),
    
    # Testing URLs (remove in production)
    path('test-file-upload/', TemplateView.as_view(template_name='file_upload_test.html'), name='test_file_upload'),
    path('simple-file-test/', TemplateView.as_view(template_name='simple_file_test.html'), name='simple_file_test'),
]
