# ChatBoard - Quick Start Guide

## 5-Minute Setup

### Windows Users

1. **Open PowerShell or Command Prompt** in the project folder

2. **Run setup script**:
   ```bash
   .\setup.bat
   ```

3. **Start the server**:
   ```bash
   python manage.py runserver
   ```

4. **Open browser**: `http://localhost:8000`

### Mac/Linux Users

1. **Open Terminal** in the project folder

2. **Run setup script**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Start the server**:
   ```bash
   python manage.py runserver
   ```

4. **Open browser**: `http://localhost:8000`

---

## Manual Setup (Step by Step)

### 1. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Setup Database

```bash
python manage.py migrate
```

### 4. Create Admin Account

```bash
python manage.py createsuperuser
```

Enter:
- Username: `admin`
- Email: `admin@example.com`
- Password: `anypassword`

### 5. Run Server

```bash
python manage.py runserver
```

### 6. Access Application

Open browser and go to:
- **Application**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **Registration**: http://localhost:8000/register/
- **Login**: http://localhost:8000/login/

---

## First Test

1. **Register User 1**:
   - Go to http://localhost:8000/register/
   - Username: `user1`
   - Email: `user1@example.com`
   - Password: `password123`

2. **Register User 2** (use different browser or incognito):
   - Go to http://localhost:8000/register/
   - Username: `user2`
   - Email: `user2@example.com`
   - Password: `password123`

3. **Login as User 1**:
   - Go to http://localhost:8000/login/
   - Username: `user1`
   - Password: `password123`

4. **Click on User 2** in dashboard sidebar

5. **Type and send a message**

6. **Open User 2 in another tab/browser**:
   - Login as user2
   - Go to chat with user1
   - See message in real-time! ✅

---

## Troubleshooting

### "Module not found" Error
```bash
# Make sure venv is activated, then:
pip install -r requirements.txt
```

### "Port 8000 already in use"
```bash
# Use different port
python manage.py runserver 8001
```

### "No such table" Error
```bash
# Run migrations again
python manage.py migrate
```

### WebSocket Not Working
- This is normal without Redis setup
- The app uses in-memory fallback
- Or install Redis (see main README)

---

## Features to Try

✅ **Register & Login** - Create multiple users

✅ **Chat in Real-Time** - Send messages instantly

✅ **View History** - Reload page, messages persist

✅ **Online Status** - See who's online (refreshes every 10s)

✅ **Admin Panel** - View all users and messages at `/admin`

✅ **Responsive Design** - Try on mobile or resize browser

---

## Useful Admin Commands

```bash
# Create another superuser
python manage.py createsuperuser

# Enter Django shell
python manage.py shell
# Then in shell:
# >>> from django.contrib.auth.models import User
# >>> User.objects.all()

# Delete database (start fresh)
# Delete db.sqlite3 file, then:
python manage.py migrate

# View all database tables
python manage.py dbshell
```

---

## Next Steps

1. **Customize Colors**: Edit `static/css/style.css`

2. **Add Your Logo**: Edit `templates/dashboard.html` and `templates/login.html`

3. **Change App Name**: Search "ChatBoard" and replace

4. **Deploy**: See README.md for deployment options

5. **Add Features**: 
   - File sharing
   - Group chats
   - Message reactions
   - Typing indicators

---

## Need Help?

1. Check the main README.md
2. Check Django documentation: https://docs.djangoproject.com/
3. Check Django Channels: https://channels.readthedocs.io/

---

**Enjoy your ChatBoard application! 💬**
