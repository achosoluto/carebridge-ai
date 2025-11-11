#!/bin/bash

# CareBridge AI Development Docker Startup Script
# This script sets up and starts the complete development environment

set -e

echo "🏥 Starting CareBridge AI Development Environment with Docker"
echo "============================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    print_error "docker-compose is not installed. Please install it and try again."
    exit 1
fi

print_status "Docker and docker-compose are available."

# Stop any existing containers
print_status "Stopping any existing containers..."
docker-compose -f docker-compose.dev.yml down -v 2>/dev/null || true

# Clean up any orphaned containers
print_status "Cleaning up orphaned containers..."
docker system prune -f > /dev/null 2>&1 || true

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p logs
mkdir -p static
mkdir -p media

# Start database and cache services first
print_status "Starting PostgreSQL and Redis services..."
docker-compose -f docker-compose.dev.yml up -d postgres redis

# Wait for database to be ready
print_status "Waiting for database to be ready..."
sleep 10

# Check if database is healthy
for i in {1..30}; do
    if docker-compose -f docker-compose.dev.yml exec postgres pg_isready -U carebridge_user -d carebridge_ai > /dev/null 2>&1; then
        print_status "Database is ready!"
        break
    fi
    if [ $i -eq 30 ]; then
        print_error "Database failed to start after 30 attempts"
        exit 1
    fi
    sleep 2
done

# Start backend service
print_status "Starting Django backend..."
docker-compose -f docker-compose.dev.yml up -d backend-dev

# Wait for backend to start
print_status "Waiting for backend to be ready..."
sleep 5

# Run database migrations
print_status "Running database migrations..."
docker-compose -f docker-compose.dev.yml exec -T backend-dev python manage.py migrate --noinput

# Load initial data if available
print_status "Loading initial data..."
docker-compose -f docker-compose.dev.yml exec -T backend-dev python manage.py init_carebridge 2>/dev/null || print_warning "Initial data script not found or failed"

# Start frontend service
print_status "Starting React frontend..."
docker-compose -f docker-compose.dev.yml up -d frontend-dev

# Start Celery worker
print_status "Starting Celery worker..."
docker-compose -f docker-compose.dev.yml up -d celery-dev

# Wait a moment for all services to fully start
sleep 5

# Health checks
print_status "Performing health checks..."

# Check backend health
if curl -f -s http://localhost:8000/api/health/ > /dev/null; then
    print_status "✅ Backend API is healthy"
else
    print_warning "⚠️  Backend API health check failed"
fi

# Check frontend
if curl -f -s http://localhost:3000/ > /dev/null; then
    print_status "✅ Frontend is accessible"
else
    print_warning "⚠️  Frontend health check failed"
fi

# Show running containers
print_status "Running containers:"
docker-compose -f docker-compose.dev.yml ps

echo ""
echo "🎉 CareBridge AI Development Environment is Ready!"
echo "================================================="
echo ""
echo "🌐 Browser URLs:"
echo "   • Frontend: http://localhost:3000"
echo "   • Backend API: http://localhost:8000"
echo "   • API Health: http://localhost:8000/api/health/"
echo "   • Admin Panel: http://localhost:8000/admin"
echo ""
echo "📝 Useful Commands:"
echo "   • View logs: docker-compose -f docker-compose.dev.yml logs -f"
echo "   • Stop services: docker-compose -f docker-compose.dev.yml down"
echo "   • Restart backend: docker-compose -f docker-compose.dev.yml restart backend-dev"
echo "   • Access backend shell: docker-compose -f docker-compose.dev.yml exec backend-dev bash"
echo "   • Access frontend shell: docker-compose -f docker-compose.dev.yml exec frontend-dev sh"
echo ""
echo "🔧 Development Notes:"
echo "   • Hot reloading is enabled for both frontend and backend"
echo "   • Database: PostgreSQL on localhost:5432"
echo "   • Cache: Redis on localhost:6379"
echo "   • All code changes will be reflected immediately"
echo ""

# Ask if user wants to open browser
read -p "Would you like to open the application in your browser? (y/N): " open_browser
if [[ $open_browser =~ ^[Yy]$ ]]; then
    if command -v open &> /dev/null; then
        open http://localhost:3000
    elif command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:3000
    else
        print_warning "Could not auto-open browser. Please visit http://localhost:3000 manually."
    fi
fi