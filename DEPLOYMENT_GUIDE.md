# ChatBoard Deployment Guide

Complete guide to deploy ChatBoard to production environments.

## Table of Contents
1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Heroku Deployment](#heroku-deployment)
3. [AWS Deployment](#aws-deployment)
4. [DigitalOcean Deployment](#digitalocean-deployment)
5. [Docker Deployment](#docker-deployment)
6. [Environment Setup](#environment-setup)
7. [Database Migration](#database-migration)
8. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Pre-Deployment Checklist

Before deploying, ensure:

- [ ] Code is tested locally
- [ ] All migrations are created (`python manage.py makemigrations`)
- [ ] Database is backed up
- [ ] Static files are collected (`python manage.py collectstatic`)
- [ ] CSRF and security settings are configured
- [ ] Environment variables are set
- [ ] Redis is available for production
- [ ] Domain name is registered
- [ ] SSL certificate is obtained

### Security Configuration

Update `chatboard/settings.py`:

```python
# Production settings
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECRET_KEY = os.environ.get('SECRET_KEY', '')  # Use environment variable!

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CORS for your domain
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]
```

---

## Heroku Deployment

### 1. Install Heroku CLI

**Windows:**
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
# Or use chocolatey
choco install heroku-cli
```

**Mac:**
```bash
brew tap heroku/brew && brew install heroku
```

**Linux:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

### 2. Login to Heroku

```bash
heroku login
```

### 3. Create Heroku App

```bash
heroku create your-app-name
```

### 4. Add PostgreSQL Add-on

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

### 5. Add Redis Add-on

```bash
heroku addons:create heroku-redis:premium-0
```

### 6. Create Procfile

Create file named `Procfile` in root directory:

```
web: gunicorn chatboard.wsgi --log-file -
worker: python manage.py process_tasks
release: python manage.py migrate
```

### 7. Create requirements.txt (already done)

Ensure it includes:
```
gunicorn==21.2.0
whitenoise==6.6.0
python-decouple==3.8
```

### 8. Set Environment Variables

```bash
heroku config:set SECRET_KEY="your-secret-key-here"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"
heroku config:set DATABASE_URL="your-postgres-url"  # Auto-set by Heroku
```

### 9. Update settings.py for Heroku

```python
import dj_database_url

# Database configuration
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Redis configuration
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
    }
}
```

### 10. Deploy

```bash
git push heroku main
```

### 11. Run Migrations

```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### 12. Verify Deployment

```bash
heroku open
```

---

## AWS Deployment

### Option A: Elastic Beanstalk

#### 1. Install EB CLI

```bash
pip install awsebcli
```

#### 2. Initialize EB

```bash
eb init -p python-3.11 chatboard --region us-east-1
```

#### 3. Create Environment

```bash
eb create chatboard-env
```

#### 4. Configure RDS (PostgreSQL)

In AWS Console:
1. Create RDS instance (PostgreSQL)
2. Create security group
3. Add to Elastic Beanstalk environment

#### 5. Configure ElastiCache (Redis)

In AWS Console:
1. Create Redis cluster
2. Add to security group
3. Note endpoint

#### 6. Update settings.py

```python
# RDS Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': '5432',
    }
}

# Redis channel layer
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(os.environ.get('REDIS_HOST'), 6379)],
        },
    }
}
```

#### 7. Create .ebextensions/django.config

```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: chatboard.wsgi:application
  aws:autoscaling:launchconfiguration:
    InstanceType: t3.micro
  aws:elasticbeanstalk:application:environment:
    PYTHONPATH: /var/app/current:$PYTHONPATH

commands:
  01_migrate:
    command: "source /var/app/venv/*/bin/activate && python manage.py migrate"
    leader_only: true
  02_collectstatic:
    command: "source /var/app/venv/*/bin/activate && python manage.py collectstatic --noinput"

container_commands:
  01_wsgipass:
    command: "sed -i 's/MODULE_DIR/var\\/app\\/current/g' /etc/nginx/conf.d/elasticbeanstalk/01_proxy.conf"
    ignoreErrors: true
```

#### 8. Deploy

```bash
eb deploy
```

#### 9. Create Superuser

```bash
eb ssh
source /var/app/venv/*/bin/activate
python manage.py createsuperuser
exit
```

---

## DigitalOcean Deployment

### Using App Platform

#### 1. Push to GitHub

```bash
git remote add origin https://github.com/yourusername/chatboard.git
git push -u origin main
```

#### 2. Connect on DigitalOcean

1. Login to DigitalOcean dashboard
2. Click "Create" → "App"
3. Select GitHub repository
4. Configure settings

#### 3. Add Database

1. Click "Create" → "Database"
2. Choose PostgreSQL
3. Add to app environment

#### 4. Add Redis

1. Click "Create" → "Database"
2. Choose Redis
3. Add connection to app

#### 5. Set Environment Variables

```
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
```

#### 6. Deploy

Click "Deploy" button and wait for deployment to complete.

### Using Droplets (Manual)

#### 1. Create Droplet

- 2GB RAM, Ubuntu 22.04 LTS

#### 2. Setup Server

```bash
# SSH into droplet
ssh root@your_droplet_ip

# Update system
apt update && apt upgrade -y

# Install Python, PostgreSQL, Redis
apt install -y python3.11 python3.11-venv postgresql redis-server nginx supervisor git

# Create app user
useradd -m -s /bin/bash chatapp
su - chatapp
```

#### 3. Clone Application

```bash
git clone https://github.com/yourusername/chatboard.git
cd chatboard
```

#### 4. Setup Environment

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 5. Configure PostgreSQL

```bash
sudo -u postgres psql
CREATE DATABASE chatboard_db;
CREATE USER chatapp WITH PASSWORD 'strong_password';
ALTER ROLE chatapp SET client_encoding TO 'utf8';
ALTER ROLE chatapp SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE chatboard_db TO chatapp;
\q
```

#### 6. Run Migrations

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

#### 7. Configure Gunicorn

Create `gunicorn_config.py`:

```python
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
max_requests = 1000
max_requests_jitter = 100
timeout = 30
```

#### 8. Configure Supervisor

Create `/etc/supervisor/conf.d/chatboard.conf`:

```ini
[program:chatboard]
directory=/home/chatapp/chatboard
command=/home/chatapp/chatboard/venv/bin/gunicorn \
  --config gunicorn_config.py \
  --chdir /home/chatapp/chatboard \
  chatboard.wsgi
user=chatapp
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/chatboard.log

[program:daphne]
directory=/home/chatapp/chatboard
command=/home/chatapp/chatboard/venv/bin/daphne \
  -b 127.0.0.1 \
  -p 8001 \
  chatboard.asgi:application
user=chatapp
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/daphne.log
```

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start all
```

#### 9. Configure Nginx

Create `/etc/nginx/sites-available/chatboard`:

```nginx
upstream django {
    server 127.0.0.1:8000;
}

upstream daphne {
    server 127.0.0.1:8001;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    client_max_body_size 10M;
    
    location /static/ {
        alias /home/chatapp/chatboard/staticfiles/;
        expires 30d;
    }
    
    location /media/ {
        alias /home/chatapp/chatboard/media/;
    }
    
    location /ws/ {
        proxy_pass http://daphne;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
    
    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/chatboard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 10. Setup SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com
```

Update Nginx config to use HTTPS.

---

## Docker Deployment

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run Daphne
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "chatboard.asgi:application"]
```

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: chatboard_db
      POSTGRES_USER: chatapp
      POSTGRES_PASSWORD: securepassword
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    ports:
      - "8000:8000"
    environment:
      DEBUG: "False"
      SECRET_KEY: "your-secret-key"
      DATABASE_URL: "postgresql://chatapp:securepassword@db:5432/chatboard_db"
      REDIS_URL: "redis://redis:6379"
    depends_on:
      - db
      - redis
    volumes:
      - .:/app

  daphne:
    build: .
    command: daphne -b 0.0.0.0 -p 8001 chatboard.asgi:application
    ports:
      - "8001:8001"
    environment:
      DEBUG: "False"
      SECRET_KEY: "your-secret-key"
      DATABASE_URL: "postgresql://chatapp:securepassword@db:5432/chatboard_db"
      REDIS_URL: "redis://redis:6379"
    depends_on:
      - db
      - redis
    volumes:
      - .:/app

volumes:
  postgres_data:
```

### Deploy

```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

## Environment Setup

### Essential Environment Variables

```
# Security
SECRET_KEY=your-long-random-secret-key
DEBUG=False

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/chatboard_db
# or for SQLite:
# DATABASE_URL=sqlite:///db.sqlite3

# Redis/Channels
REDIS_URL=redis://localhost:6379/0

# Domain
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Email (optional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# SSL
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### .env File

Create `.env` in root directory:

```bash
cp .env.example .env
# Edit .env with production values
```

### Load in settings.py

```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost').split(',')
```

---

## Database Migration

### PostgreSQL Migration

1. **Export SQLite data**:
```bash
python manage.py dumpdata > dump.json
```

2. **Update settings.py** to use PostgreSQL

3. **Run migrations**:
```bash
python manage.py migrate
```

4. **Load data**:
```bash
python manage.py loaddata dump.json
```

### Backup Database

```bash
# PostgreSQL
pg_dump chatboard_db > backup.sql

# Restore
psql chatboard_db < backup.sql
```

---

## Monitoring & Maintenance

### Log Monitoring

```bash
# Supervisor logs
tail -f /var/log/chatboard.log
tail -f /var/log/daphne.log

# System logs
journalctl -u nginx -f
journalctl -u supervisor -f
```

### Performance Monitoring

- Use Sentry for error tracking
- Use New Relic for APM
- Use Datadog for monitoring
- Use UptimeRobot for uptime monitoring

### Regular Maintenance

```bash
# Update Python packages
pip install --upgrade -r requirements.txt

# Database backups (daily)
pg_dump chatboard_db > backups/backup_$(date +%Y%m%d).sql

# Clear old sessions
python manage.py clearsessions

# Vacuum database (monthly)
python manage.py shell
>>> from django.core.management import call_command
>>> call_command('clearsessions')

# Monitor disk space
df -h
du -sh /home/chatapp/chatboard
```

### Security Updates

```bash
# Update system packages
sudo apt update && apt upgrade -y

# Update Python packages
pip install --upgrade pip setuptools wheel
pip install -U -r requirements.txt

# Check for vulnerabilities
pip install safety
safety check
```

---

## SSL/HTTPS Setup

### Let's Encrypt (Free)

```bash
sudo apt install certbot
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com
```

### Auto-renewal

```bash
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

### Update Nginx

```nginx
listen 443 ssl;
ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

# HTTP redirect
server {
    listen 80;
    return 301 https://$server_name$request_uri;
}
```

---

## Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check Redis is running
redis-cli ping  # Should return PONG
```

### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
sudo systemctl restart nginx
```

### WebSocket Connection Issues
```bash
# Check Daphne is running
sudo supervisorctl status daphne

# Check port is open
netstat -tlnp | grep 8001
```

### Permission Issues
```bash
# Fix file permissions
sudo chown -R chatapp:chatapp /home/chatapp/chatboard
sudo chmod -R 755 /home/chatapp/chatboard
```

---

## Performance Tips

1. **Enable caching**: Redis for sessions
2. **Use CDN**: CloudFlare for static files
3. **Optimize database**: Add indexes, use select_related
4. **Compress responses**: Enable gzip
5. **Monitor resources**: CPU, memory, disk
6. **Scale horizontally**: Load balancer for multiple servers

---

**Deploy with confidence! 🚀**
