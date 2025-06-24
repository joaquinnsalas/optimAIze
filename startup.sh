#!/bin/bash

# OptimAIze Unified Startup Script
# This script sets up and runs OptimAIze in different environments

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"
DATA_DIR="$SCRIPT_DIR/data"
CONFIG_DIR="$SCRIPT_DIR/config"
LOGS_DIR="$SCRIPT_DIR/logs"

# Default environment
ENVIRONMENT=${ENVIRONMENT:-"local"}
PORT=${PORT:-8000}
HOST=${HOST:-"0.0.0.0"}

print_banner() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════╗"
    echo "║           OptimAIze Setup            ║"
    echo "║    Production-Grade RAG System       ║"
    echo "╚══════════════════════════════════════╝"
    echo -e "${NC}"
}

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_dependencies() {
    log_info "Checking system dependencies..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is required but not installed"
        exit 1
    fi
    
    # Check Python version
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    if ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)"; then
        log_error "Python 3.9+ required, found $PYTHON_VERSION"
        exit 1
    fi
    
    log_info "Python $PYTHON_VERSION found ✓"
    
    # Check Docker (optional)
    if command -v docker &> /dev/null; then
        log_info "Docker found ✓"
        DOCKER_AVAILABLE=true
    else
        log_warn "Docker not found - Docker deployment won't be available"
        DOCKER_AVAILABLE=false
    fi
}

setup_directories() {
    log_info "Setting up directories..."
    
    mkdir -p "$DATA_DIR/input"
    mkdir -p "$DATA_DIR/output" 
    mkdir -p "$DATA_DIR/logs"
    mkdir -p "$LOGS_DIR"
    mkdir -p "$CONFIG_DIR"
    
    # Create default config if it doesn't exist
    if [ ! -f "$CONFIG_DIR/config.yaml" ]; then
        log_info "Creating default configuration..."
        cat > "$CONFIG_DIR/config.yaml" << 'EOF'
app:
  name: "OptimAIze"
  version: "1.0.0"
  log_level: "INFO"

indexing:
  input_directory: "./data/input"
  chunk_size: 1000
  chunk_overlap: 200
  batch_size: 10
  supported_extensions: [".pdf", ".docx", ".pptx", ".xlsx", ".txt", ".md"]

embeddings:
  model_name: "all-MiniLM-L6-v2"
  dimension: 384
  device: "cpu"
  batch_size: 32

retrieval:
  fusion_method: "rrf"
  top_k_per_source: 20
  final_top_k: 10
  min_similarity_threshold: 0.0
  rrf_k: 60
  concurrent_search: true

qdrant:
  url: "http://localhost:6333"
  collection_name: "optimaize_vectors"
  distance_metric: "cosine"

elasticsearch:
  url: "http://localhost:9200"
  index_name: "optimaize_keywords"
  analyzer: "standard"

database:
  type: "sqlite"
  url: "sqlite:///./data/optimaize.db"

llm:
  default_model: "llama3"
  ollama_url: "http://localhost:11434"
  temperature: 0.7
  max_tokens: 2048
  timeout_seconds: 30

api:
  host: "0.0.0.0"
  port: 8000
  cors_origins: ["*"]
  docs_url: "/docs"
EOF
        log_info "Default config created at $CONFIG_DIR/config.yaml"
    fi
    
    log_info "Directories setup complete ✓"
}

setup_python_environment() {
    log_info "Setting up Python environment..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "$VENV_DIR" ]; then
        log_info "Creating virtual environment..."
        python3 -m venv "$VENV_DIR"
    fi
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    
    # Upgrade pip
    log_info "Upgrading pip..."
    pip install --upgrade pip > /dev/null 2>&1
    
    # Install requirements
    if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
        log_info "Installing Python dependencies..."
        pip install -r "$SCRIPT_DIR/requirements.txt"
        log_info "Dependencies installed ✓"
    else
        log_error "requirements.txt not found!"
        exit 1
    fi
}

setup_external_services() {
    case "$ENVIRONMENT" in
        "docker")
            setup_docker_services
            ;;
        "azure")
            setup_azure_services
            ;;
        "local")
            setup_local_services
            ;;
        *)
            log_error "Unknown environment: $ENVIRONMENT"
            exit 1
            ;;
    esac
}

setup_local_services() {
    log_info "Setting up local services..."
    
    # Check if services are already running
    if curl -s http://localhost:6333/health > /dev/null 2>&1; then
        log_info "Qdrant already running ✓"
    else
        log_warn "Qdrant not running - you'll need to start it manually"
        log_info "Run: docker run -p 6333:6333 -p 6334:6334 -v \$(pwd)/qdrant_storage:/qdrant/storage:z qdrant/qdrant:v1.7.4"
    fi
    
    if curl -s http://localhost:9200/_cluster/health > /dev/null 2>&1; then
        log_info "Elasticsearch already running ✓"
    else
        log_warn "Elasticsearch not running - you'll need to start it manually"
        log_info "Run: docker run -p 9200:9200 -e \"discovery.type=single-node\" -e \"xpack.security.enabled=false\" docker.elastic.co/elasticsearch/elasticsearch:8.11.0"
    fi
    
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        log_info "Ollama already running ✓"
    else
        log_warn "Ollama not running - LLM features will be limited"
        log_info "Install Ollama: curl -fsSL https://ollama.ai/install.sh | sh"
    fi
}

setup_docker_services() {
    log_info "Setting up Docker services..."
    
    if [ "$DOCKER_AVAILABLE" != true ]; then
        log_error "Docker is required for Docker environment"
        exit 1
    fi
    
    # Start services using docker-compose
    if [ -f "$SCRIPT_DIR/docker-compose.yml" ]; then
        log_info "Starting Docker services..."
        docker-compose up -d qdrant elasticsearch ollama
        
        # Wait for services to be ready
        log_info "Waiting for services to start..."
        sleep 10
        
        # Check service health
        for i in {1..30}; do
            if curl -s http://localhost:6333/health > /dev/null 2>&1 && \
               curl -s http://localhost:9200/_cluster/health > /dev/null 2>&1; then
                log_info "Services ready ✓"
                break
            fi
            if [ $i -eq 30 ]; then
                log_error "Services failed to start"
                exit 1
            fi
            sleep 2
        done
    else
        log_error "docker-compose.yml not found!"
        exit 1
    fi
}

setup_azure_services() {
    log_info "Azure environment detected..."
    
    # Azure Web Apps will provide these through environment variables
    export QDRANT_URL=${QDRANT_URL:-"http://localhost:6333"}
    export ELASTICSEARCH_URL=${ELASTICSEARCH_URL:-"http://localhost:9200"}
    export OLLAMA_URL=${OLLAMA_URL:-"http://localhost:11434"}
    
    log_info "Using external services (Azure-managed)"
    log_info "Qdrant URL: $QDRANT_URL"
    log_info "Elasticsearch URL: $ELASTICSEARCH_URL" 
    log_info "Ollama URL: $OLLAMA_URL"
}

initialize_database() {
    log_info "Initializing database..."
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    
    # Run database initialization
    python3 main.py status > /dev/null 2>&1 || true
    
    log_info "Database initialized ✓"
}

show_usage() {
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  setup     - Full setup (dependencies, services, database)"
    echo "  start     - Start the API server"
    echo "  index     - Run document indexing"
    echo "  status    - Show system status"
    echo "  clean     - Clean up (stop services, remove venv)"
    echo "  docker    - Start with Docker services"
    echo "  help      - Show this help"
    echo ""
    echo "Environment Variables:"
    echo "  ENVIRONMENT - local|docker|azure (default: local)"
    echo "  PORT        - API port (default: 8000)"
    echo "  HOST        - API host (default: 0.0.0.0)"
    echo ""
    echo "Examples:"
    echo "  $0 setup              # Full setup"
    echo "  $0 start              # Start API server"
    echo "  ENVIRONMENT=docker $0 docker  # Use Docker"
    echo "  PORT=3000 $0 start    # Start on port 3000"
}

start_api_server() {
    log_info "Starting OptimAIze API server..."
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    
    # Set environment variables
    export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"
    export API_HOST="$HOST"
    export API_PORT="$PORT"
    
    log_info "🚀 Starting server at http://$HOST:$PORT"
    log_info "📚 API docs at http://$HOST:$PORT/docs"
    log_info "🔍 Health check at http://$HOST:$PORT/health"
    echo ""
    log_info "Press Ctrl+C to stop"
    
    # Start the server
    python3 api_server.py
}

run_indexing() {
    log_info "Running document indexing..."
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    
    # Set environment variables
    export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"
    
    # Run indexing
    python3 main.py index "$@"
}

show_status() {
    log_info "Checking OptimAIze status..."
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    
    # Set environment variables
    export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"
    
    # Show status
    python3 main.py status
}

cleanup() {
    log_info "Cleaning up..."
    
    # Stop Docker services if running
    if [ -f "$SCRIPT_DIR/docker-compose.yml" ] && [ "$DOCKER_AVAILABLE" = true ]; then
        docker-compose down
    fi
    
    # Remove virtual environment
    if [ -d "$VENV_DIR" ]; then
        rm -rf "$VENV_DIR"
        log_info "Virtual environment removed"
    fi
    
    log_info "Cleanup complete ✓"
}

# Main execution
main() {
    print_banner
    
    case "${1:-setup}" in
        "setup")
            check_dependencies
            setup_directories
            setup_python_environment
            setup_external_services
            initialize_database
            log_info "🎉 Setup complete! Run './startup.sh start' to begin"
            ;;
        "start")
            start_api_server
            ;;
        "index")
            shift
            run_indexing "$@"
            ;;
        "status")
            show_status
            ;;
        "docker")
            ENVIRONMENT="docker"
            check_dependencies
            setup_directories
            setup_python_environment
            setup_external_services
            initialize_database
            start_api_server
            ;;
        "clean")
            cleanup
            ;;
        "help"|"--help"|"-h")
            show_usage
            ;;
        *)
            log_error "Unknown command: $1"
            show_usage
            exit 1
            ;;
    esac
}

# Run main function
main "$@"