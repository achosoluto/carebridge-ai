# CareBridge AI Docker Deployment Guide

This guide provides complete Docker deployment setup for CareBridge AI to solve browser visibility issues and provide a stable, isolated development environment.

## 🏗️ Architecture Overview

The Docker deployment consists of:

- **Frontend**: React + Vite + Nginx (Production) / React + Vite (Development)
- **Backend**: Django + REST Framework 
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Background Tasks**: Celery Worker
- **Network**: Isolated Docker network for secure communication

## 🚀 Quick Start (Development)

### Prerequisites
- Docker and Docker Compose installed
- At least 4GB RAM available
- Ports 3000, 8000, 5432, 6379 available

### Step 1: Start Development Environment

```bash
# Stop any existing services
docker-compose down -v

# Start development services with hot reloading
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f
```

### Step 2: Initialize Database

```bash
# Run migrations
docker-compose -f docker-compose.dev.yml exec backend-dev python manage.py migrate

# Create superuser (optional)
docker-compose -f docker-compose.dev.yml exec backend-dev python manage.py createsuperuser

# Load initial data
docker-compose -f docker-compose.dev.yml exec backend-dev python manage.py init_carebridge
```

### Step 3: Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **API Documentation**: http://localhost:8000/api/docs/

## 🚀 Production Deployment

### Step 1: Build and Start Production Environment

```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# Initialize database
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py init_carebridge
```

### Step 2: Verify Deployment

```bash
# Check all services are running
docker-compose ps

# Check health of all containers
docker-compose exec backend curl -f http://localhost:8000/api/health/
curl -f http://localhost:3000/health
```

## 🔧 Available Commands

### Development Workflow

```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up -d

# View logs in real-time
docker-compose -f docker-compose.dev.yml logs -f

# Stop development environment
docker-compose -f docker-compose.dev.yml down

# Rebuild specific service
docker-compose -f docker-compose.dev.yml up -d --build frontend-dev

# Access container shells
docker-compose -f docker-compose.dev.yml exec backend-dev bash
docker-compose -f docker-compose.dev.yml exec frontend-dev sh

# Run Django commands
docker-compose -f docker-compose.dev.yml exec backend-dev python manage.py <command>

# Run frontend commands
docker-compose -f docker-compose.dev.yml exec frontend-dev npm run <command>
```

### Production Commands

```bash
# Start production
docker-compose up -d

# Stop all services
docker-compose down

# Restart specific service
docker-compose restart backend

# View logs
docker-compose logs -f [service_name]

# Scale services
docker-compose up -d --scale celery=2

# Backup database
docker-compose exec postgres pg_dump -U carebridge_user carebridge_ai > backup.sql

# Restore database
docker exec -i carebridge_postgres psql -U carebridge_user -d carebridge_ai < backup.sql
```

## 🌐 Browser Access URLs

### Development Environment
| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | React Application |
| Backend API | http://localhost:8000/api/ | REST API |
| Admin Panel | http://localhost:8000/admin | Django Admin |
| API Docs | http://localhost:8000/api/docs/ | Swagger Documentation |
| Health Check | http://localhost:3000/health | Frontend Health |
| Health Check | http://localhost:8000/api/health/ | Backend Health |

### Production Environment
| Service | URL | Purpose |
|---------|-----|---------|
| Application | http://localhost:3000 | Full-stack Application |
| API | http://localhost:3000/api/ | API Proxy |
| Admin | http://localhost:3000/admin | Admin Panel |
| Health | http://localhost:3000/health | Health Check |

## 🔍 Health Checks and Monitoring

### Automated Health Checks
All services include built-in health checks:

```bash
# Check overall system health
curl http://localhost:3000/health

# Check backend health
curl http://localhost:8000/api/health/

# Check database connectivity
docker-compose exec backend python manage.py check --database default

# Check Redis connectivity  
docker-compose exec redis redis-cli ping
```

### Log Monitoring
```bash
# Real-time logs for all services
docker-compose logs -f

# Specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
docker-compose logs -f celery

# Last 100 lines of logs
docker-compose logs --tail=100 backend
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Find process using port
lsof -i :3000
lsof -i :8000

# Kill process or change port in docker-compose.yml
```

#### 2. Database Connection Issues
```bash
# Check database container
docker-compose exec postgres psql -U carebridge_user -d carebridge_ai -c "SELECT 1;"

# Reset database
docker-compose down -v
docker-compose up -d postgres
```

#### 3. Frontend Build Issues
```bash
# Rebuild frontend
docker-compose build frontend
docker-compose up -d frontend

# Clear node modules (development)
docker-compose -f docker-compose.dev.yml down
rm -rf frontend/node_modules
docker-compose -f docker-compose.dev.yml up -d
```

#### 4. Backend Issues
```bash
# Check migrations
docker-compose exec backend python manage.py showmigrations

# Apply migrations
docker-compose exec backend python manage.py migrate

# Collect static files
docker-compose exec backend python manage.py collectstatic --noinput
```

#### 5. CORS Issues
The CORS configuration is set up for Docker networking. If you encounter issues:

- Ensure `CORS_ALLOWED_ORIGINS` includes your frontend URL
- Check that containers are on the same Docker network
- Verify environment variables are properly set

### Performance Optimization

#### For Development
- Use `docker-compose.dev.yml` for hot reloading
- Volume mounting for live code updates
- Development builds with source maps

#### For Production
- Multi-stage Docker builds
- Nginx static file serving
- Connection pooling
- Redis caching
- Health checks and monitoring

## 📱 API Endpoints Testing

All 12 API endpoints should be accessible through the Docker setup:

```bash
# Test main API endpoints
curl -X GET http://localhost:8000/api/patients/
curl -X GET http://localhost:8000/api/appointments/
curl -X GET http://localhost:8000/api/messages/
curl -X GET http://localhost:8000/api/doctors/
curl -X GET http://localhost:8000/api/dashboard/metrics/

# Test through frontend proxy
curl -X GET http://localhost:3000/api/patients/
curl -X GET http://localhost:3000/api/appointments/
```

## 🔒 Security Considerations

### Development Environment
- Debug mode enabled
- CORS configured for localhost
- SQLite fallback available
- No SSL/HTTPS

### Production Environment
- Debug mode disabled
- Secure CORS configuration
- PostgreSQL required
- Environment variables for secrets
- Nginx for static file serving

## 🚀 Next Steps

1. **Environment Setup**: Copy `.env.example` to `.env` and configure as needed
2. **SSL/HTTPS**: Configure SSL certificates for production
3. **Load Balancing**: Scale services as needed
4. **Monitoring**: Add application monitoring (e.g., Prometheus, Grafana)
5. **Backup Strategy**: Implement automated database backups
6. **CI/CD**: Set up continuous integration and deployment

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all ports are available
3. Ensure Docker and Docker Compose are up to date
4. Check system resources (memory, disk space)
5. Review container logs for detailed error messages