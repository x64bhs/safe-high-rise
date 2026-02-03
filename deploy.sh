#!/bin/bash

# Quick deployment script for Safe High-Rise
# Usage: ./deploy.sh [option]
# Options: docker, local, build-frontend

set -e

case "$1" in
  docker)
    echo "🚀 Deploying with Docker..."
    docker-compose up -d --build
    echo "✅ Deployment complete! Access at http://localhost"
    ;;
  local)
    echo "🚀 Starting local development..."
    echo "Starting backend..."
    cd backend
    if [ ! -d "venv" ]; then
      python -m venv venv
    fi
    source venv/bin/activate 2>/dev/null || venv\Scripts\activate
    pip install -r requirements.txt
    uvicorn main:app --reload --port 8000 &
    BACKEND_PID=$!
    cd ..
    
    echo "Starting frontend..."
    cd frontend
    npm install
    npm run dev &
    FRONTEND_PID=$!
    cd ..
    
    echo "✅ Backend running on http://localhost:8000 (PID: $BACKEND_PID)"
    echo "✅ Frontend running on http://localhost:5173 (PID: $FRONTEND_PID)"
    echo "Press Ctrl+C to stop both services"
    wait
    ;;
  build-frontend)
    echo "🏗️  Building frontend for production..."
    cd frontend
    npm install
    npm run build
    echo "✅ Build complete! Output in frontend/dist/"
    ;;
  *)
    echo "Usage: ./deploy.sh [option]"
    echo "Options:"
    echo "  docker          - Deploy using Docker Compose"
    echo "  local           - Start local development servers"
    echo "  build-frontend  - Build frontend for production"
    exit 1
    ;;
esac


