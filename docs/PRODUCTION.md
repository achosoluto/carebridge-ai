# Production Deployment Guide

## Prerequisites
- Docker and Docker Compose installed on the host machine.

## Architecture
- **Backend**: Django with Gunicorn (Workers: 3)
- **Database**: PostgreSQL 15
- **Frontend**: Nginx serving React Static Build
- **Orchestration**: Docker Compose

## Running with Docker Compose

1. **Build and Run**:
   ```bash
   docker-compose up --build -d
   ```

2. **Access the Application**:
   - **Frontend**: http://localhost:5173
   - **Backend API**: http://localhost:8000/api/

3. **Database**:
   - Automatically managed by the `db` service (PostgreSQL).
   - Data persisted in `postgres_data` volume.

4. **Startup Process**:
   - The backend runs `start.sh` which:
     - Runs migrations (`migrate`)
     - Creates default superuser (`admin`)
     - Collects static files (`collectstatic`)
     - Starts Gunicorn

## Environment Variables
For production, verify the following in `docker-compose.yml`:
- `DEBUG=0`
- `SECRET_KEY`: [Secure Random String]
- `ALLOWED_HOSTS`: [Your Domain]
- `DB_ENGINE`: `django.db.backends.postgresql`
