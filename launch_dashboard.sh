#!/bin/bash

# CareBridge AI Dashboard Launch Script
# This script starts both the Django backend and React frontend servers

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default ports
BACKEND_PORT=8000
FRONTEND_PORT=3000

# Process IDs
BACKEND_PID=""
FRONTEND_PID=""

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if a port is available
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 1  # Port is in use
    else
        return 0  # Port is available
    fi
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to wait for service to be ready
wait_for_service() {
    local port=$1
    local service=$2
    local timeout=30
    local count=0
    
    print_status "Waiting for $service to start on port $port..."
    
    while [ $count -lt $timeout ]; do
        if nc -z localhost $port; then
            print_success "$service is ready on port $port"
            return 0
        fi
        sleep 2
        ((count++))
    done
    
    print_error "Timeout waiting for $service on port $port"
    return 1
}

# Function to start the backend server
start_backend() {
    print_status "Starting Django backend server on port $BACKEND_PORT..."
    
    # Check if port is available
    if ! check_port $BACKEND_PORT; then
        print_error "Port $BACKEND_PORT is already in use. Please stop the existing process or change the port."
        return 1
    fi
    
    # Check if Python and Django are available
    if ! command_exists python3; then
        print_error "Python3 is not installed or not in PATH"
        return 1
    fi
    
    if ! python3 -c "import django" 2>/dev/null; then
        print_error "Django is not installed or not accessible"
        return 1
    fi
    
    # Source environment variables if they exist
    if [ -f ".env" ]; then
        print_status "Loading environment variables from .env"
        export $(grep -v '^#' .env | xargs)
    fi
    
    # Start the Django development server in the background
    python3 manage.py runserver 0.0.0.0:$BACKEND_PORT &
    BACKEND_PID=$!
    
    # Verify the backend started successfully
    if ! wait_for_service $BACKEND_PORT "Backend"; then
        kill $BACKEND_PID 2>/dev/null || true
        return 1
    fi
    
    print_success "Backend server started successfully with PID $BACKEND_PID"
    return 0
}

# Function to start the frontend server
start_frontend() {
    print_status "Starting React frontend server on port $FRONTEND_PORT..."
    
    # Check if port is available
    if ! check_port $FRONTEND_PORT; then
        print_error "Port $FRONTEND_PORT is already in use. Please stop the existing process or change the port."
        return 1
    fi
    
    # Check if Node.js and npm are available
    if ! command_exists node; then
        print_error "Node.js is not installed or not in PATH"
        return 1
    fi
    
    if ! command_exists npm; then
        print_error "npm is not installed or not in PATH"
        return 1
    fi
    
    # Check if frontend directory exists
    if [ ! -d "frontend" ]; then
        print_error "frontend directory not found"
        return 1
    fi
    
    # Source environment variables if they exist
    if [ -f "frontend/.env" ]; then
        print_status "Loading environment variables from frontend/.env"
        export $(grep -v '^#' frontend/.env | xargs)
    elif [ -f ".env" ]; then
        print_status "Loading environment variables from .env"
        export $(grep -v '^#' .env | xargs)
    fi
    
    # Check if node_modules exists, install dependencies if not
    if [ ! -d "frontend/node_modules" ]; then
        print_status "Installing frontend dependencies..."
        cd frontend && npm install && cd ..
    fi
    
    # Start the Vite development server in the background
    cd frontend && npm run dev -- --port $FRONTEND_PORT --host 0.0.0.0 &
    FRONTEND_PID=$!
    cd ..
    
    # Verify the frontend started successfully
    if ! wait_for_service $FRONTEND_PORT "Frontend"; then
        kill $FRONTEND_PID 2>/dev/null || true
        return 1
    fi
    
    print_success "Frontend server started successfully with PID $FRONTEND_PID"
    return 0
}

# Function to stop all servers
stop_servers() {
    print_status "Stopping servers..."
    
    if [ ! -z "$BACKEND_PID" ]; then
        print_status "Stopping backend server (PID: $BACKEND_PID)..."
        kill $BACKEND_PID 2>/dev/null || true
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        print_status "Stopping frontend server (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    
    print_success "Servers stopped"
}

# Function to trap Ctrl+C and stop servers
cleanup() {
    echo ""
    print_warning "Received interrupt signal. Stopping servers..."
    stop_servers
    exit 0
}

# Set up signal trap for graceful shutdown
trap cleanup SIGINT SIGTERM

# Main execution
main() {
    print_status "Starting CareBridge AI Dashboard..."
    print_status "Backend will run on port $BACKEND_PORT"
    print_status "Frontend will run on port $FRONTEND_PORT"
    
    # Start backend first
    if ! start_backend; then
        print_error "Failed to start backend server. Exiting."
        exit 1
    fi
    
    # Start frontend
    if ! start_frontend; then
        print_error "Failed to start frontend server. Stopping backend and exiting."
        stop_servers
        exit 1
    fi
    
    print_success "Both servers are running!"
    print_status "Backend: http://localhost:$BACKEND_PORT"
    print_status "Frontend: http://localhost:$FRONTEND_PORT"
    print_status "Press Ctrl+C to stop the servers"
    
    # Wait for both processes
    wait $BACKEND_PID $FRONTEND_PID
}

# Run main function
main "$@"