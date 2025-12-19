
# ChatBoard - Real-time Chat Application

A modern, real-time chat application built with Django backend and vanilla JavaScript frontend. Features WebSocket-based messaging, user authentication, and a responsive UI similar to WhatsApp/Telegram.

## Features

✅ **User Authentication**
- User registration with validation
- Secure login/logout system
- Profile management

✅ **Real-time Messaging**
- WebSocket-based instant messaging via Django Channels
- One-to-one private chats
- Message timestamps
- Auto-scrolling chat interface

✅ **User Management**
- View all registered users
- Online/offline status indicator
- User profiles with names and emails

✅ **Database Integration**
- SQLite for development (easily upgradeable to PostgreSQL)
- Message history persistence
- Unread message tracking

✅ **Responsive Design**
- Modern WhatsApp/Telegram-style UI
- Mobile-friendly interface
- Dark/Light theme compatible

✅ **REST API**
- Get users list
- Fetch chat history
- Send messages
- Update online status

## Project Structure

```
chatboard/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── chatboard/               # Django project settings
│   ├── __init__.py
│   ├── settings.py          # Main Django settings
│   ├── asgi.py              # ASGI config for Channels
│   ├── wsgi.py              # WSGI config
│   └── urls.py              # Main URL router
├── chat/                    # Main chat app
│   ├── migrations/          # Database migrations
│   ├── __init__.py
│   ├── admin.py             # Admin panel config
│   ├── apps.py              # App config
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── api_views.py         # REST API views
│   ├── consumers.py         # WebSocket consumers
│   ├── routing.py           # WebSocket URL routing
│   ├── serializers.py       # DRF serializers
│   ├── urls.py              # App URL routing
│   └── api_urls.py          # API URL routing
├── templates/               # HTML templates
│   ├── login.html           # Login page
│   ├── register.html        # Registration page
│   ├── dashboard.html       # Main dashboard
│   └── chat.html            # Chat interface
├── static/                  # Static files
│   ├── css/
│   │   ├── auth.css         # Authentication styles
│   │   └── style.css        # Main styles
│   └── js/
│       ├── chat.js          # Chat functionality
│       └── dashboard.js     # Dashboard functionality
└── db.sqlite3              # SQLite database (created after migration)
```

## Prerequisites

- Python 3.10 or higher
- pip package manager
- Redis (optional, for production - fallback to in-memory for development)
- Windows/Mac/Linux OS

## Installation & Setup

### 1. Create Virtual Environment

**Windows (PowerShell/CMD):**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Navigate to Project Directory

```bash
cd chatboard
```

### 4. Run Database Migrations

Create the database tables:
```bash
python manage.py migrate
```

### 5. Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account. Example:
```
Username: admin
Email: admin@example.com
Password: ••••••••
Password (again): ••••••••
Superuser created successfully.
```

### 6. Collect Static Files (Optional for Development)

```bash
python manage.py collectstatic --noinput
```

## Running the Application

### Option A: Development with In-Memory Channels (No Redis Required)

This is the simplest setup for development. Edit `chatboard/settings.py` and replace the Redis channel layer config with:

```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}
```

Then run:
```bash
python manage.py runserver
```

The application will be available at: `http://localhost:8000`

### Option B: Development with Redis (Recommended for Testing)

1. **Install Redis:**

   **Windows:**
   - Download from: https://github.com/microsoftarchive/redis/releases
   - Or use Windows Subsystem for Linux (WSL)

   **Mac:**
   ```bash
   brew install redis
   ```

   **Linux:**
   ```bash
   sudo apt-get install redis-server
   ```

2. **Start Redis:**

   **Windows (using WSL or Redis installer):**
   ```bash
   redis-server
   ```

   **Mac/Linux:**
   ```bash
   redis-server
   ```

3. **Run Django with Daphne (ASGI server):**

   ```bash
   daphne -b 0.0.0.0 -p 8000 chatboard.asgi:application
   ```

   Or use the runserver (which uses Daphne automatically):
   ```bash
   python manage.py runserver
   ```

The application will be available at: `http://localhost:8000`

## Usage Guide

### 1. Register New Account

1. Go to `http://localhost:8000/register/`
2. Fill in the registration form:
   - Username (unique)
   - Email (unique)
   - Password (minimum 6 characters)
   - Confirm password
   - First name (optional)
   - Last name (optional)
3. Click "Register" button
4. You'll be redirected to login page

### 2. Login

1. Go to `http://localhost:8000/login/`
2. Enter your username and password
3. Click "Login" button
4. You'll be redirected to the dashboard

### 3. View Dashboard

On the dashboard:
- **Left sidebar**: Shows all registered users with online/offline status
- **Main area**: Welcome message and feature overview
- Click any user to open the chat window

### 4. Start Chatting

1. Click on a user from the sidebar
2. You'll enter the chat interface
3. Type your message in the input box
4. Click "Send" button or press Ctrl+Enter (Cmd+Enter on Mac)
5. Messages appear in real-time
6. Previous messages load automatically from the database
7. Click the back button (←) to return to dashboard

### 5. View Admin Panel

1. Go to `http://localhost:8000/admin/`
2. Login with your superuser credentials
3. You can:
   - View all users and their profiles
   - View all messages in the system
   - Mark messages as read
   - Update user online status

## API Endpoints

The application provides REST API endpoints:

### Get Users List
```
GET /api/users/
Headers: Authorization (Session)
Response: List of all users (except current user)
```

### Get Chat History
```
GET /api/messages/history/?other_user_id=2
Headers: Authorization (Session)
Response: All messages between two users
```

### Send Message via API
```
POST /api/messages/send/
Headers: Authorization (Session)
Content-Type: application/json
Body: {
    "receiver_id": 2,
    "message_text": "Hello!"
}
Response: Created message object
```

### Update Online Status
```
PATCH /api/status/
Headers: Authorization (Session)
Content-Type: application/json
Body: {
    "is_online": true
}
Response: Updated status
```

## Configuration

### Database

The project uses SQLite by default. To use PostgreSQL in production:

1. Install psycopg2: `pip install psycopg2-binary`
2. Update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'chatboard_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Channel Layers

For production, configure Redis:

```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('redis-server-address', 6379)],
        },
    }
}
```

## Security Considerations

⚠️ **Important for Production:**

1. **Change SECRET_KEY** in `settings.py`:
   ```python
   SECRET_KEY = 'your-long-random-secret-key'
   ```

2. **Set DEBUG = False** in `settings.py`

3. **Set ALLOWED_HOSTS** properly:
   ```python
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   ```

4. **Use HTTPS** (configure with proper SSL certificates)

5. **Environment Variables** for sensitive data:
   ```python
   import os
   from dotenv import load_dotenv
   load_dotenv()
   SECRET_KEY = os.getenv('SECRET_KEY')
   ```

6. **CSRF Protection**: Already enabled (all forms use {% csrf_token %})

7. **XSS Protection**: Messages are HTML-escaped in JavaScript

## Troubleshooting

### WebSocket Connection Issues

**Problem**: Messages not sending or receiving
**Solution**:
1. Check browser console for errors (F12)
2. Ensure you're using the correct protocol (ws:// for HTTP, wss:// for HTTPS)
3. Check if Django Channels is properly configured
4. Restart the server

### Migration Issues

**Problem**: `"no such table"` error
**Solution**:
```bash
python manage.py migrate
python manage.py migrate chat
```

### Port Already in Use

**Problem**: `Address already in use` error
**Solution**:
```bash
# Use a different port
python manage.py runserver 8001

# Or kill the process using port 8000
# Windows: netstat -ano | findstr :8000
# Mac/Linux: lsof -i :8000
```

### Database Lock Error

**Problem**: SQLite database is locked
**Solution**:
- Delete `db.sqlite3` and re-run migrations
- Or use PostgreSQL for production

## Extending the Application

### Add File Sharing

Modify `Message` model:
```python
file = models.FileField(upload_to='chat_files/', null=True, blank=True)
```

### Add Group Chats

Create a `ChatGroup` model and update consumers

### Add Typing Indicator

Send `typing` event through WebSocket

### Add Message Search

Use Django's full-text search

### Add Message Reactions

Create a `Reaction` model linked to messages

## Performance Optimization

1. **Database Indexing**: Already added for common queries
2. **Pagination**: Implement for large chat histories
3. **Caching**: Use Redis for user sessions
4. **Static File CDN**: Serve CSS/JS from CDN
5. **Image Optimization**: Compress user avatars

## Deployment Options

### Heroku
```bash
heroku create your-app-name
git push heroku main
heroku run python manage.py migrate
```

### AWS (EB, EC2, etc.)
- Use PostgreSQL on RDS
- Use ElastiCache for Redis
- Configure Elastic Load Balancer
- Use CloudFront for static files

### DigitalOcean
- Deploy with App Platform or Droplets
- Configure PostgreSQL Managed Database
- Use Spaces for static files

## Common Commands

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Access admin panel
http://localhost:8000/admin/

# Run development server
python manage.py runserver

# Run with specific port
python manage.py runserver 8001

# Create new app
python manage.py startapp app_name

# Enter Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic

# Check for issues
python manage.py check

# Show active migrations
python manage.py showmigrations
```

## Testing

To run tests:
```bash
python manage.py test chat
```

To run with verbose output:
```bash
python manage.py test chat -v 2
```

## Contributing

Feel free to extend this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open-source and available under the MIT License.

## Support

For issues, questions, or suggestions:
1. Check existing documentation
2. Review Django Channels documentation
3. Check Django REST Framework docs
4. Open an issue on the repository

## Version History

- **v1.0.0** (2024) - Initial release
  - User authentication
  - Real-time messaging with WebSockets
  - Message history
  - Online status
  - REST API
  - Responsive UI

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Channels Documentation](https://channels.readthedocs.io/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [WebSocket Documentation](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [Redis Documentation](https://redis.io/docs/)

---

**Happy Chatting! 💬**
=======
# ChatBorad
ChatBoard ek smart AI-powered communication platform hai jo real-time chat, group discussion, voice messages aur productivity tools ko ek jagah par laata hai. Isme advanced search, online status, emoji reactions aur speech-to-text jaise features milte hain, jo students aur teams ke liye fast, simple aur efficient collaboration possible banate hain.

