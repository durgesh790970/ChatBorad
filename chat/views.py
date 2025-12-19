"""
Views for chat app - handles user authentication and chat pages.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db import models
from django.utils import timezone
from datetime import datetime
from .models import Message
import json


@require_http_methods(["GET", "POST"])
def register_view(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        # Validate inputs
        if not all([username, email, password, confirm_password]):
            messages.error(request, 'All fields are required.')
            return render(request, 'register.html')

        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'register.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'register.html')

        # Create user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'register.html')

    return render(request, 'register.html')


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Update online status
            user.profile.is_online = True
            user.profile.save()
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')

    return render(request, 'login.html')


@login_required(login_url='login')
def logout_view(request):
    """Handle user logout"""
    # Update online status
    request.user.profile.is_online = False
    request.user.profile.save()
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


@login_required(login_url='login')
def dashboard_view(request):
    """Display dashboard with list of all users sorted by recent messages"""
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
            models.Q(sender=current_user, receiver=user) |
            models.Q(sender=user, receiver=current_user)
        ).order_by('-timestamp').first()
        
        latest_timestamp = latest_message.timestamp if latest_message else None
        
        user_data.append({
            'user': user,
            'unread_count': unread_count,
            'latest_timestamp': latest_timestamp
        })
    
    # Sort by latest message (most recent first)
    # Use a very old date as default for users with no messages
    min_date = datetime.min.replace(tzinfo=timezone.utc)
    user_data.sort(key=lambda x: x['latest_timestamp'] or min_date, reverse=True)

    context = {
        'user_data': user_data,
        'current_user': current_user,
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def chat_view(request, user_id):
    """Display chat page for one-to-one conversation"""
    try:
        other_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('dashboard')

    if other_user == request.user:
        messages.error(request, 'You cannot chat with yourself.')
        return redirect('dashboard')

    current_user = request.user

    # Fetch chat history
    chat_messages = Message.objects.filter(
        (models.Q(sender=current_user) & models.Q(receiver=other_user)) |
        (models.Q(sender=other_user) & models.Q(receiver=current_user))
    ).order_by('timestamp')

    # Mark received messages as read
    received_messages = chat_messages.filter(
        sender=other_user,
        receiver=current_user,
        is_read=False
    )
    received_messages.update(is_read=True)

    # Get all users except current user for the sidebar
    all_users = User.objects.exclude(id=current_user.id).order_by('first_name', 'last_name')

    context = {
        'other_user': other_user,
        'current_user': current_user,
        'messages': chat_messages,
        'users': all_users,
    }
    return render(request, 'chat.html', context)


@login_required(login_url='login')
def ai_chat_view(request):
    """Display AI chat page with WhatsApp-like interface"""
    current_user = request.user
    context = {
        'current_user': current_user,
    }
    return render(request, 'ai_chat.html', context)


@login_required(login_url='login')
def online_status_view(request):
    """Display online status page for all users"""
    current_user = request.user
    context = {
        'current_user': current_user,
    }
    return render(request, 'online_status.html', context)


@login_required(login_url='login')
def api_online_status(request):
    """API endpoint to get online status of all users with real-time data"""
    from django.http import JsonResponse
    
    current_user = request.user
    all_users = User.objects.exclude(id=current_user.id).prefetch_related('profile')
    
    users_data = []
    for user in all_users:
        # Determine user status based on profile
        # In a real app, this would be tracked via WebSocket activity
        is_online = user.profile.is_online
        
        # Default status based on is_online flag
        if is_online:
            status = 'online'
        else:
            status = 'offline'
        
        # Count messages sent by this user
        message_count = Message.objects.filter(sender=user).count()
        
        # Get last seen time
        last_message = Message.objects.filter(
            models.Q(sender=user) | models.Q(receiver=user)
        ).order_by('-timestamp').first()
        last_seen = last_message.timestamp if last_message else user.date_joined
        
        full_name = f"{user.first_name} {user.last_name}".strip() or user.username
        
        users_data.append({
            'id': user.id,
            'name': full_name,
            'username': user.username,
            'status': status,
            'is_online': is_online,
            'message_count': message_count,
            'last_seen': last_seen.isoformat() if last_seen else None,
            'joined_date': user.date_joined.isoformat(),
        })
    
    return JsonResponse({
        'users': users_data,
        'total_count': len(users_data),
        'timestamp': timezone.now().isoformat()
    })
