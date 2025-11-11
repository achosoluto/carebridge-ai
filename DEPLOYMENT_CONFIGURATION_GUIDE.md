# CareBridge AI - Deployment & Configuration Guide

## Overview

This guide provides step-by-step instructions for deploying CareBridge AI in production environments, from development setup to full production deployment with scaling considerations.

---

## Prerequisites

### System Requirements
- **Operating System**: Linux (Ubuntu 20.04+ recommended) or macOS
- **Python**: 3.11+ 
- **Node.js**: 18+ and npm
- **Database**: PostgreSQL 13+ (production) or SQLite (development)
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 20GB available space
- **Network**: Internet connection for external API access

### External Services Required
- **Google Translate API**: For translation services
- **SMS Service**: Twilio, AWS SNS, or similar for notifications
- **Email Service**: SendGrid, AWS SES, or similar
- **Chat Platform APIs**: KakaoTalk, WeChat, LINE (optional)

---

## Development Environment Setup

### 1. Clone and Setup Repository

```bash
# Clone the repository
git clone <repository-url>
cd carebridge-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
cd frontend
npm install
cd ..
```

### 2. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
```

**Required Environment Variables:**

```env
# Django Settings
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/carebridge_ai
# For development: DATABASE_URL=sqlite:///db.sqlite3

# Google Translate API
GOOGLE_TRANSLATE_API_KEY=your-google-translate-api-key

# Notification Services
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=your-twilio-phone-number

SENDGRID_API_KEY=your-sendgrid-api-key
SENDGRID_FROM_EMAIL=noreply@your-domain.com

# Chat Platform APIs (Optional)
KAKAO_CLIENT_ID=your-kakao-client-id
WECHAT_APP_ID=your-wechat-app-id
LINE_CHANNEL_ID=your-line-channel-id

# Redis Configuration (for caching)
REDIS_URL=redis://localhost:6379/0

# Logging
LOG_LEVEL=INFO
```

### 3. Database Setup

```bash
# Create database
createdb carebridge_ai

# Run migrations
python manage.py migrate

# Initialize Phase 2 data
python manage.py init_phase2_data

# Create superuser (optional)
python manage.py createsuperuser
```

### 4. Run Development Servers

```bash
# Terminal 1: Backend
python manage.py runserver 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

**Access Points:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Admin Interface: http://localhost:8000/admin

---

## Production Deployment

### Option 1: Docker Deployment (Recommended)

#### 1. Create Production Docker Configuration

**Dockerfile:**
```dockerfile
# Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "config.wsgi:application"]
```

**docker-compose.production.yml:**
```yaml
version: '3.8'

services:
  backend:
    build: 
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=${DATABASE_URL}
      - GOOGLE_TRANSLATE_API_KEY=${GOOGLE_TRANSLATE_API_KEY}
    depends_on:
      - database
      - redis
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped

  database:
    image: postgres:13
    environment:
      - POSTGRES_DB=carebridge_ai
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    restart: unless-stopped

  redis:
    image: redis:6-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

#### 2. Deploy with Docker

```bash
# Create production environment file
cp .env.example .env.production
# Edit .env.production with production values

# Build and start services
docker-compose -f docker-compose.production.yml up -d

# View logs
docker-compose -f docker-compose.production.yml logs -f
```

### Option 2: Manual Production Deployment

#### 1. Server Setup (Ubuntu 20.04)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install PM2 for process management
sudo npm install -g pm2
```

#### 2. Database Setup

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE carebridge_ai;
CREATE USER carebridge_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE carebridge_ai TO carebridge_user;
\q
```

#### 3. Application Deployment

```bash
# Create application directory
sudo mkdir -p /var/www/carebridge-ai
sudo chown $USER:$USER /var/www/carebridge-ai
cd /var/www/carebridge-ai

# Clone repository
git clone <repository-url> .

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Collect static files
python manage.py collectstatic --noinput

# Setup database
python manage.py migrate
python manage.py init_phase2_data
```

#### 4. Gunicorn Configuration

**Create gunicorn configuration:**
```bash
mkdir -p /var/www/carebridge-ai/logs
```

**gunicorn.conf.py:**
```python
# gunicorn.conf.py
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 50
preload_app = True
daemon = False
pidfile = "/var/www/carebridge-ai/logs/gunicorn.pid"
user = "www-data"
group = "www-data"
accesslog = "/var/www/carebridge-ai/logs/access.log"
errorlog = "/var/www/carebridge-ai/logs/error.log"
loglevel = "info"
```

#### 5. PM2 Process Management

**ecosystem.config.js:**
```javascript
module.exports = {
  apps: [{
    name: 'carebridge-backend',
    script: 'gunicorn',
    args: '--config gunicorn.conf.py config.wsgi:application',
    cwd: '/var/www/carebridge-ai',
    env: {
      DJANGO_SETTINGS_MODULE: 'config.settings',
      PYTHONPATH: '/var/www/carebridge-ai'
    },
    instances: 1,
    exec_mode: 'fork',
    watch: false,
    max_memory_restart: '1G',
    error_file: '/var/www/carebridge-ai/logs/pm2-error.log',
    out_file: '/var/www/carebridge-ai/logs/pm2-out.log'
  }]
};
```

```bash
# Start application
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

#### 6. Nginx Configuration

**/etc/nginx/sites-available/carebridge-ai:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /var/www/carebridge-ai/frontend/dist;
        try_files $uri $uri/ /index.html;
        
        # Cache static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support for real-time features
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Admin interface
    location /admin/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/carebridge-ai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 7. SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

---

## Environment-Specific Configurations

### Development Environment
```env
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
LOG_LEVEL=DEBUG
CACHE_BACKEND=django.core.cache.backends.dummy.DummyCache
```

### Staging Environment
```env
DEBUG=False
ALLOWED_HOSTS=staging.your-domain.com
DATABASE_URL=postgresql://user:pass@staging-db:5432/carebridge_staging
LOG_LEVEL=INFO
CACHE_BACKEND=django.core.cache.backends.redis.RedisCache
REDIS_URL=redis://staging-redis:6379/1
```

### Production Environment
```env
DEBUG=False
ALLOWED_HOSTS=your-domain.com,api.your-domain.com
DATABASE_URL=postgresql://user:pass@prod-db:5432/carebridge_ai
LOG_LEVEL=WARNING
CACHE_BACKEND=django.core.cache.backends.redis.RedisCache
REDIS_URL=redis://prod-redis:6379/0
SESSION_ENGINE=django.contrib.sessions.backends.cache
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_CONTENT_TYPE_NOSNIFF=True
X_FRAME_OPTIONS=DENY
```

---

## API Keys Configuration

### Google Translate API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing
3. Enable Google Translate API
4. Create credentials (API Key)
5. Restrict API key to Google Translate API
6. Add to environment variables

### Notification Services

#### Twilio (SMS)
1. Sign up at [Twilio](https://www.twilio.com/)
2. Get Account SID and Auth Token
3. Purchase phone number
4. Configure environment variables

#### SendGrid (Email)
1. Sign up at [SendGrid](https://sendgrid.com/)
2. Create API key
3. Verify sender domain
4. Configure environment variables

#### Chat Platforms
- **KakaoTalk**: Apply for Kakao Developer account
- **WeChat**: Register WeChat Official Account
- **LINE**: Apply for LINE Developer account

---

## Monitoring and Logging

### 1. Application Monitoring

```python
# settings.py monitoring configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/carebridge-ai/django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
    },
}
```

### 2. Health Check Endpoints

Add to `urls.py`:
```python
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache

def health_check(request):
    """Health check endpoint for load balancers"""
    try:
        # Check database
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        # Check cache
        cache.set('health_check', 'ok', 10)
        cache.get('health_check')
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected',
            'cache': 'working',
            'timestamp': timezone.now().isoformat()
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': timezone.now().isoformat()
        }, status=503)
```

### 3. Performance Monitoring

```python
# Add to middleware.py
import time
from django.urls import resolve

class PerformanceMonitoringMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        
        response = self.get_response(request)
        
        duration = time.time() - start_time
        view_name = resolve(request.path).view_name
        
        # Log slow requests
        if duration > 1.0:
            logger.warning(f"Slow request: {view_name} took {duration:.2f}s")
        
        # Add performance header
        response['X-Response-Time'] = f"{duration:.3f}s"
        
        return response
```

---

## Backup and Recovery

### 1. Database Backup

```bash
#!/bin/bash
# backup_database.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/carebridge-ai"
mkdir -p $BACKUP_DIR

# PostgreSQL backup
pg_dump $DATABASE_URL > $BACKUP_DIR/carebridge_db_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/carebridge_db_$DATE.sql

# Keep only last 7 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete

echo "Database backup completed: carebridge_db_$DATE.sql.gz"
```

### 2. File Backup

```bash
#!/bin/bash
# backup_files.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/carebridge-ai"

# Backup media files
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /var/www/carebridge-ai/media/

# Keep only last 7 days
find $BACKUP_DIR -name "media_*.tar.gz" -mtime +7 -delete
```

### 3. Automated Backup Cron Jobs

```bash
# Add to crontab
crontab -e

# Daily database backup at 2 AM
0 2 * * * /var/www/carebridge-ai/scripts/backup_database.sh

# Weekly file backup on Sunday at 3 AM
0 3 * * 0 /var/www/carebridge-ai/scripts/backup_files.sh
```

---

## Scaling Considerations

### 1. Horizontal Scaling

```yaml
# docker-compose.scale.yml for load balancing
version: '3.8'
services:
  backend:
    build: .
    deploy:
      replicas: 3
    environment:
      - DATABASE_URL=${DATABASE_URL}
    depends_on:
      - database
      
  nginx-lb:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx-lb.conf:/etc/nginx/nginx.conf
    depends_on:
      - backend
```

### 2. Database Scaling

```bash
# Read replica configuration
# In settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'carebridge_ai',
        'USER': 'carebridge_user',
        'PASSWORD': 'password',
        'HOST': 'primary-db',
        'PORT': '5432',
    },
    'replica': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'carebridge_ai',
        'USER': 'carebridge_user',
        'PASSWORD': 'password',
        'HOST': 'replica-db',
        'PORT': '5432',
    }
}
```

### 3. Cache Scaling

```bash
# Redis cluster setup
# redis-cluster.conf
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
appendonly yes
```

---

## Troubleshooting

### Common Issues

#### 1. Database Connection Errors
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection
psql -h localhost -U carebridge_user -d carebridge_ai
```

#### 2. Translation API Issues
```bash
# Test Google Translate API
curl -H "Content-Type: application/json" \
     -d '{"q":"Hello","target":"ko"}' \
     "https://translation.googleapis.com/language/translate/v2?key=YOUR_API_KEY"
```

#### 3. Permission Issues
```bash
# Fix file permissions
sudo chown -R www-data:www-data /var/www/carebridge-ai
sudo chmod -R 755 /var/www/carebridge-ai
```

#### 4. Memory Issues
```bash
# Monitor memory usage
htop
free -m

# Adjust Gunicorn workers
# In gunicorn.conf.py: workers = max(2, multiprocessing.cpu_count() * 2 + 1)
```

### Log Analysis

```bash
# Django application logs
tail -f /var/log/carebridge-ai/django.log

# Nginx access logs
tail -f /var/log/nginx/access.log

# Nginx error logs
tail -f /var/log/nginx/error.log

# Gunicorn logs
tail -f /var/www/carebridge-ai/logs/error.log
```

---

## Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Set DEBUG=False in production
- [ ] Configure ALLOWED_HOSTS
- [ ] Use HTTPS (SSL certificate)
- [ ] Set strong database passwords
- [ ] Configure firewall (UFW)
- [ ] Regular security updates
- [ ] API key restrictions
- [ ] File permission validation
- [ ] Log monitoring setup

---

## Maintenance

### Regular Tasks
1. **Weekly**: Review application logs
2. **Monthly**: Update system packages
3. **Quarterly**: Security audit
4. **Semi-annually**: Performance review
5. **Annually**: Full system backup verification

### Update Process
```bash
# Update application
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
pm2 restart carebridge-backend
```

---

**Deployment Guide Version**: 2.0  
**Last Updated**: November 11, 2025  
**Status**: Production Ready