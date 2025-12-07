# CareBridge AI - Healthcare Communication Platform

CareBridge is a healthcare communication platform that enables multi-language patient-staff interactions with real-time translation.

## Features
- Multi-language patient support (Japanese, Chinese, Korean, English)
- Real-time message translation between patients and medical staff
- Appointment management system
- Patient record management

## Tech Stack
- Backend: Django, Django REST Framework, PostgreSQL
- Frontend: React, TypeScript, Tailwind CSS
- Translation: Google Cloud Translation API
- Deployment: Docker, Docker Compose

## Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd carebridge-ai
```

2. Start the development environment:
```bash
docker-compose up --build
```

3. Access the application:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Django Admin: http://localhost:8000/admin (admin/password)

## Production Deployment

### Prerequisites
- Docker and Docker Compose
- Domain name pointing to your server
- SSL certificate (recommended)

### Deployment Steps

1. Clone the repository on your production server:
```bash
git clone <repository-url>
cd carebridge-ai
```

2. Configure environment variables:
```bash
cp backend/.env.prod backend/.env
# Edit backend/.env with your production settings
```

3. Update docker-compose.yml with your production settings:
- Change ALLOWED_HOSTS
- Set appropriate SECRET_KEY
- Configure PostgreSQL credentials
- Consider adding SSL termination with nginx

4. Build and start the services:
```bash
docker-compose up --build -d
```

5. Create an admin user (optional, one was created during startup):
```bash
docker-compose exec backend python manage.py createsuperuser
```

### Production Considerations

- **Security**: Change all default passwords and use strong, unique values
- **SSL**: Use a reverse proxy like nginx with SSL termination
- **Database**: Regular backups of the PostgreSQL database
- **Environment Variables**: Never commit sensitive information to version control
- **Monitoring**: Add health checks and monitoring as needed

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DEBUG | Enable/disable debug mode | 0 (production) |
| SECRET_KEY | Django secret key | Required for production |
| ALLOWED_HOSTS | Allowed hostnames | Comma-separated list |
| DB_ENGINE | Database engine | django.db.backends.postgresql |
| DB_NAME | Database name | carebridge |
| DB_USER | Database user | postgres |
| DB_PASSWORD | Database password | postgres |
| DB_HOST | Database host | db |
| DB_PORT | Database port | 5432 |

## API Endpoints

- `/api-token-auth/` - Get authentication token
- `/patients/` - Patient CRUD operations (requires auth)
- `/doctors/` - Doctor information
- `/appointments/` - Appointment management
- `/messages/` - Message and translation operations
- `/public/doctors/` - Public doctor information (no auth required)
- `/public/appointments/` - Public appointment booking (no auth required)

## Default Credentials

For initial access:
- Username: `admin`
- Password: `password`

**Important**: Change the default admin password immediately after deployment.

## Architecture

The application follows a clean architecture:
- Frontend: React with TypeScript
- Backend: Django REST API
- Database: PostgreSQL
- Translation: Google Cloud Translation API
- Deployment: Docker containers with Compose orchestration