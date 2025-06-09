# OptimAIze - Enterprise RAG System

**A production-ready Retrieval-Augmented Generation (RAG) system for enterprise document search and AI-powered question answering.**

## 🚀 Quick Start

### Prerequisites
- Docker Desktop
- Git
- 8GB+ RAM recommended

### Setup (5 minutes)

1. **Clone the repository:**
```bash
git clone https://github.com/joaquinnsalas/optimAIze.git
cd optimAIze
```

2. **Start all services:**
```bash
docker compose up -d
```

3. **Download the LLM model:**
```bash
docker exec optimaize-ollama ollama pull llama3
```

4. **Verify everything is running:**
```bash
curl http://localhost:8000/health
```

5. **Access the admin portal:**
- URL: `http://localhost:8001`
- Login: `admin@optimaize.com` / `admin123`

### 🎯 You're Ready!
- **Main API**: `http://localhost:8000` - Document search and AI chat
- **Admin Portal**: `http://localhost:8001` - System management and analytics
- **Ollama**: `http://localhost:11434` - Local LLM inference

---

## 🏗️ System Architecture

Our enterprise-grade RAG system follows this architecture:

```
Client (Web App, Slack, Teams, API)
        |
        ↓
Enterprise SSO & Role-Based Access
        └──> Auth via SAML/OAuth2 (e.g., Azure AD, Okta)
        └──> Role-based document and feature permissions

Retrieval Engine
        ├── Qdrant → Semantic Vector Search (nomic-embed-text)
        ├── Elasticsearch → Keyword Index (BM25-style)
        └── Fusion Layer:
              ├── RRF (Reciprocal Rank Fusion)
              └── ML Reranker (local model, trained on usage logs or clicks)

Prompt Engine
        ├── Input: Top-k chunks
        ├── Autosuggestion → (real-time UI hinting)
        ├── Query Rewrite → (LLM-aided improved phrasing)
        └── Prompt formatting via templates

LLM Executor
        ├── Default: Ollama (LLaMA 3 8B)
        ├── Swap-in options: Claude, GPT-4o, Mistral, Mixtral
        └── Configurable per org or user group

LLM Response Handler
        ├── Answer synthesis
        ├── Attach citations & snippets
        └── Fallback logic for missing answers

🧾 Logging & Analytics (for admin panel)
        ├── Prompt + Response text
        ├── Model used (name + version)
        ├── Runtime (ms), tokens used, embedding latency
        ├── User ID, Timestamp, Org
        └── User feedback

Frontend UI
        ├── Chat interface w/ streaming + citations
        ├── Upload page (permitted formats + folders)
        ├── Admin dashboard (usage logs, config, model choice)
        └── File system interface (team-based folders like "Engineer Docs")
```

---

## 🛠️ Development Guide

### Project Structure
```
optimAIze/
├── app/                    # Main FastAPI application
│   ├── api/               # API routes
│   ├── core/              # Core business logic
│   ├── services/          # External service integrations
│   └── models/            # Data models
├── admin/                 # Admin portal (FastAPI)
│   ├── templates/         # Jinja2 templates
│   ├── static/           # CSS/JS assets
│   └── main.py           # Admin app entry point
├── docker-compose.yml     # Multi-service orchestration
├── Dockerfile             # Main app container
├── admin.Dockerfile       # Admin portal container
└── requirements.txt       # Python dependencies
```

### Core Services

#### 1. **Main API** (`app/`) - Port 8000
- **FastAPI** application for document indexing and search
- **Endpoints:**
  - `POST /index` - Index documents
  - `POST /search` - Search documents
  - `POST /generate` - AI question answering
  - `GET /health` - System health check

#### 2. **Admin Portal** (`admin/`) - Port 8001
- **Management interface** for system configuration
- **Features:**
  - Real-time analytics dashboard
  - System settings management
  - Template configuration
  - User activity monitoring

#### 3. **Qdrant** - Port 6333
- **Vector database** for semantic search
- Stores document embeddings using `nomic-embed-text`
- Enables similarity-based document retrieval

#### 4. **Elasticsearch** - Port 9200
- **Search engine** for keyword-based search
- BM25 scoring for traditional text matching
- Complements vector search for hybrid retrieval

#### 5. **Ollama** - Port 11434
- **Local LLM inference** server
- Default model: LLaMA 3 8B
- Configurable for different models per use case

### Development Workflow

#### 1. **Making Changes**
```bash
# Edit code in app/ or admin/
# Rebuild affected services
docker compose build --no-cache optimaize-app
docker compose up -d optimaize-app

# View logs
docker compose logs -f optimaize-app
```

#### 2. **Adding New Features**
```bash
# For API changes
edit app/api/routes.py
edit app/core/search.py

# For admin changes  
edit admin/main.py
edit admin/templates/

# Test changes
curl http://localhost:8000/new-endpoint
```

#### 3. **Debugging**
```bash
# Check service status
docker compose ps

# View logs for specific service
docker compose logs --tail=50 optimaize-app
docker compose logs --tail=50 optimaize-admin

# Access service shell
docker exec -it optimaize-app bash
```

### Testing

#### API Testing
```bash
# Health check
curl http://localhost:8000/health

# Index a document
curl -X POST http://localhost:8000/index \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a test document", "metadata": {"title": "Test"}}'

# Search documents
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "test document", "limit": 5}'

# Generate AI response
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"query": "What is in the test document?"}'
```

#### Admin Portal Testing
```bash
# Login test
curl -X POST http://localhost:8001/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email=admin@optimaize.com&password=admin123"

# Dashboard access (after login)
curl -H "Cookie: access_token=YOUR_TOKEN" http://localhost:8001/
```

---

## 🔧 Configuration

### Environment Variables
Create `.env` file for custom configuration:

```bash
# Database
ELASTICSEARCH_URL=http://elasticsearch:9200
QDRANT_URL=http://qdrant:6333

# LLM Settings
OLLAMA_URL=http://ollama:11434
DEFAULT_MODEL=llama3

# Security
JWT_SECRET_KEY=your-secret-key-here
ADMIN_EMAIL=admin@yourcompany.com
ADMIN_PASSWORD=secure-password

# Embedding Model
EMBEDDING_MODEL=nomic-embed-text
EMBEDDING_DIMENSION=768

# Search Settings
DEFAULT_TOP_K=10
SEARCH_MODE=hybrid  # hybrid, semantic, keyword
```

### Model Configuration
```bash
# List available models
docker exec optimaize-ollama ollama list

# Pull new model
docker exec optimaize-ollama ollama pull mistral

# Remove old model
docker exec optimaize-ollama ollama rm llama3
```

---

## 📊 Monitoring & Analytics

### Health Monitoring
```bash
# Check all services
curl http://localhost:8000/health

# Individual service health
curl http://localhost:9200/_cluster/health  # Elasticsearch
curl http://localhost:6333/health           # Qdrant
curl http://localhost:11434/api/ps          # Ollama
```

### Performance Metrics
Access the admin dashboard at `http://localhost:8001` to view:
- Query response times
- Token usage statistics
- Model performance metrics
- User activity logs
- System resource usage

---

## 🚨 Troubleshooting

### Common Issues

#### 1. **Services won't start**
```bash
# Check Docker resources
docker system df
docker system prune

# Restart services
docker compose down
docker compose up -d
```

#### 2. **Out of memory errors**
```bash
# Check memory usage
docker stats

# Increase Docker memory limit in Docker Desktop settings
# Recommended: 8GB+ for full system
```

#### 3. **Search not working**
```bash
# Check Elasticsearch
curl http://localhost:9200/_cluster/health

# Check Qdrant
curl http://localhost:6333/health

# Rebuild search indices
curl -X POST http://localhost:8000/reindex
```

#### 4. **LLM not responding**
```bash
# Check Ollama status
docker exec optimaize-ollama ollama list

# Pull model if missing
docker exec optimaize-ollama ollama pull llama3

# Check model memory usage
docker exec optimaize-ollama ollama ps
```

### Debug Mode
```bash
# Enable debug logging
export OLLAMA_DEBUG=INFO
docker compose up -d

# View detailed logs
docker compose logs -f optimaize-app
```

---

## 🔒 Security Considerations

### Production Deployment

1. **Change default credentials:**
```bash
# Update admin credentials in .env
ADMIN_EMAIL=admin@yourcompany.com
ADMIN_PASSWORD=your-secure-password
```

2. **Configure SSL/TLS:**
```yaml
# In docker-compose.yml
services:
  optimaize-app:
    environment:
      - HTTPS_ENABLED=true
      - SSL_CERT_PATH=/certs/cert.pem
      - SSL_KEY_PATH=/certs/key.pem
```

3. **Set up reverse proxy:**
```nginx
# nginx.conf
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
    }
    
    location /admin {
        proxy_pass http://localhost:8001;
    }
}
```

---

## 🤝 Contributing

### Development Setup
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and test locally
docker compose up -d
# Test your changes...

# Commit and push
git add .
git commit -m "Add your feature description"
git push origin feature/your-feature-name

# Create pull request
```

### Code Style
- **Python**: Follow PEP 8, use `black` formatter
- **FastAPI**: Use type hints and Pydantic models
- **HTML/CSS**: Follow Bootstrap conventions
- **JavaScript**: Use modern ES6+ syntax

### Pull Request Template
```markdown
## Description
Brief description of changes

## Testing
- [ ] API endpoints tested
- [ ] Admin portal tested
- [ ] Docker build successful
- [ ] All services start correctly

## Breaking Changes
List any breaking changes
```

---

## 📋 Roadmap

### Current Features ✅
- Hybrid search (semantic + keyword)
- Local LLM inference with Ollama
- Admin dashboard with analytics
- Document indexing and retrieval
- JWT authentication

### Planned Features 🚧
- [ ] Enterprise SSO integration (SAML/OAuth2)
- [ ] Role-based access control
- [ ] Advanced reranking models
- [ ] Real-time chat interface
- [ ] Document upload UI
- [ ] Team-based folder organization
- [ ] Query autosuggestion
- [ ] Advanced analytics and reporting

### Integration Roadmap 🔮
- [ ] Slack/Teams integration
- [ ] API client libraries
- [ ] Kubernetes deployment
- [ ] Cloud provider integrations
- [ ] Advanced security features

---

## 📞 Support

### Getting Help
1. **Check this README** for common solutions
2. **Review logs** using `docker compose logs`
3. **Create GitHub issue** with detailed error information
4. **Contact the team** via Slack #optimaize-support

### Team Contacts
- **Technical Lead**: @joaquinnsalas
- **DevOps**: @your-devops-team
- **Product**: @your-product-team

---

## 📄 License

This project is proprietary software. See [LICENSE](LICENSE) for details.

---

*Built with ❤️ by the OptimAIze team*