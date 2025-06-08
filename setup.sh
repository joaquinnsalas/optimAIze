#!/bin/bash

# OptimAIze Quick Setup Script
# This script sets up the entire OptimAIze system with Docker

set -e  # Exit on any error

echo "🚀 OptimAIze Setup Script"
echo "========================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first:"
    echo "   https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first:"
    echo "   https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose found"

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data/input data/output data/logs admin/static admin/templates

# Start services
echo "🐳 Starting Docker services..."
docker-compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to start..."
sleep 30

# Check service health
echo "🔍 Checking service health..."

# Check Qdrant
if curl -sf http://localhost:6333/health > /dev/null; then
    echo "✅ Qdrant is running"
else
    echo "❌ Qdrant is not responding"
fi

# Check Elasticsearch
if curl -sf http://localhost:9200/_cluster/health > /dev/null; then
    echo "✅ Elasticsearch is running"
else
    echo "❌ Elasticsearch is not responding"
fi

# Check Ollama
if curl -sf http://localhost:11434/api/tags > /dev/null; then
    echo "✅ Ollama is running"
else
    echo "❌ Ollama is not responding"
fi

# Check Admin Portal
if curl -sf http://localhost:8001/api/health > /dev/null; then
    echo "✅ Admin Portal is running"
else
    echo "❌ Admin Portal is not responding"
fi

# Install default LLM model
echo "🤖 Installing LLM model (llama3)..."
docker-compose exec -T ollama ollama pull llama3

echo ""
echo "🎉 Setup Complete!"
echo ""
echo "Services running:"
echo "• Main API: http://localhost:8000"
echo "• Admin Portal: http://localhost:8001"
echo "• Default admin login: admin@optimaize.com / admin123"
echo ""
echo "Next steps:"
echo "1. Add documents: cp your-documents/* data/input/"
echo "2. Index documents: docker-compose exec optimaize python main.py index"
echo "3. Ask questions: docker-compose exec optimaize python main.py ask \"Your question?\""
echo "4. Manage system: Open http://localhost:8001 in your browser"
echo ""
echo "For help: docker-compose exec optimaize python main.py --help"
echo "To stop: docker-compose down"