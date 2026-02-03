@echo off
REM Quick deployment script for Safe High-Rise (Windows)
REM Usage: deploy.bat [option]
REM Options: docker, local, build-frontend

setlocal

if "%1"=="docker" goto docker
if "%1"=="local" goto local
if "%1"=="build-frontend" goto build-frontend
goto usage

:docker
echo 🚀 Deploying with Docker...
docker-compose up -d --build
echo ✅ Deployment complete! Access at http://localhost
goto end

:local
echo 🚀 Starting local development...
echo Starting backend...
cd backend
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate
pip install -r requirements.txt
start "Backend Server" cmd /k "uvicorn main:app --reload --port 8000"
cd ..
echo Starting frontend...
cd frontend
call npm install
start "Frontend Server" cmd /k "npm run dev"
cd ..
echo ✅ Backend running on http://localhost:8000
echo ✅ Frontend running on http://localhost:5173
echo Both servers started in separate windows. Close them manually when done.
goto end

:build-frontend
echo 🏗️  Building frontend for production...
cd frontend
call npm install
call npm run build
echo ✅ Build complete! Output in frontend/dist/
cd ..
goto end

:usage
echo Usage: deploy.bat [option]
echo Options:
echo   docker          - Deploy using Docker Compose
echo   local           - Start local development servers
echo   build-frontend  - Build frontend for production
goto end

:end
endlocal


