@echo off
echo Starting Gridwise AI in Development Mode...

REM Check if docker-compose is installed
where docker-compose >nul 2>nul
if %errorlevel% neq 0 (
    echo docker-compose could not be found. Please install it.
    exit /b 1
)

REM Ensure .env exists
if not exist .env (
    echo Copying .env.example to .env...
    copy .env.example .env
)

REM Start services
echo Starting services...
docker-compose -f docker-compose.yml -f infra/docker/docker-compose.yml up --build -d

echo Services started!
echo Backend: http://localhost:8000
echo ML API: http://localhost:8001
echo Frontend: http://localhost:80
echo To view logs, run: docker-compose logs -f
