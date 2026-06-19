#!/bin/bash
echo "Starting Gridwise AI in Development Mode..."

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null
then
    echo "docker-compose could not be found. Please install it."
    exit 1
fi

# Ensure .env exists
if [ ! -f .env ]; then
    echo "Copying .env.example to .env..."
    cp .env.example .env
fi

# Start services
echo "Starting services..."
docker-compose -f docker-compose.yml -f infra/docker/docker-compose.yml up --build -d

echo "Services started!"
echo "Backend: http://localhost:8000"
echo "ML API: http://localhost:8001"
echo "Frontend: http://localhost:80"
echo "To view logs, run: docker-compose logs -f"
