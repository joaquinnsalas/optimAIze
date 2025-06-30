# OptimAIze Setup Guide

This guide will help you set up OptimAIze locally and deploy to Azure.

## 🚀 Quick Start (Local)

### Prerequisites
- Python 3.9+
- Git
- Docker (optional, for services)

### 1. Clone and Setup

```bash
# Clone your repository
git clone https://github.com/joaquinnsalas/optimAIze.git
cd optimAIze

# Make startup script executable
chmod +x startup.sh

# Run full setup
./startup.sh setup
```

This will:
- ✅ Check dependencies
- ✅ Create virtual environment
- ✅ Install Python packages
- ✅ Set up directories and config
- ✅ Initialize database

### 2. Start Services

**Option A: Use Docker (Recommended)**
```bash
# Start with Docker services
./startup.sh docker
```

**Option B: Manual Service Setup**
```bash
# Start Qdrant
docker run -d -p 6333:6333 -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage:z \
  qdrant/qdrant:v1.7.4

# Start Elasticsearch  
docker run -d -p 9200:9200 -p 9300:9300 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  docker.elastic.co/elasticsearch/elasticsearch:8.11.0

# Install and start Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve &
ollama pull llama3

# Start OptimAIze API
./startup.sh start
```

### 3. Index Your Documents

```bash
# Add documents to data/input directory
cp /path/to/your/documents/* data/input/

# Run indexing
./startup.sh index

# Check status
./startup.sh status
```

### 4. Test the API

```bash
# Check health
curl http://localhost:8000/health

# Search documents
curl "http://localhost:8000/search?q=your+search+query"

# View API docs
open http://localhost:8000/docs
```

## 🌐 Azure Deployment

### Prerequisites
- Azure CLI installed and logged in
- Azure subscription with appropriate permissions

### 1. Deploy to Azure

```bash
# Make deployment script executable
chmod +x deploy-azure.sh

# Set your app name (must be globally unique)
export WEB_APP_NAME="optimaize-yourcompany-$(date +%s)"

# Deploy everything
./deploy-azure.sh deploy
```

This will:
- ✅ Create Azure Resource Group
- ✅ Create App Service Plan (Linux B1)
- ✅ Create Web App with Python 3.11
- ✅ Configure startup commands
- ✅ Deploy your code via Git
- ✅ Set up placeholder external services

### 2. Configure External Services

After deployment, you need to set up the external services:

**Option A: Azure Container Instances**
```bash
# Create Qdrant container
az container create \
  --resource-group optimaize-rg \
  --name qdrant-instance \
  --image qdrant/qdrant:v1.7.4 \
  --ports 6333 6334 \
  --dns-name-label qdrant-optimaize

# Create Elasticsearch container  
az container create \
  --resource-group optimaize-rg \
  --name elasticsearch-instance \
  --image docker.elastic.co/elasticsearch/elasticsearch:8.11.0 \
  --ports 9200 9300 \
  --environment-variables 'discovery.type=single-node' 'xpack.security.enabled=false' \
  --dns-name-label elasticsearch-optimaize

# Update Web App settings with real URLs
az webapp config appsettings set \
  --resource-group optimaize-rg \
  --name $WEB_APP_NAME \
  --settings \
  QDRANT_URL="http://qdrant-optimaize.eastus.azurecontainer.io:6333" \
  ELASTICSEARCH_URL="http://elasticsearch-optimaize.eastus.azurecontainer.io:9200"
```

**Option B: Azure Native Services**
```bash
# Use Azure AI Search instead of Elasticsearch
az search service create \
  --resource-group optimaize-rg \
  --name optimaize-search \
  --sku standard

# Update settings to use Azure services
az webapp config appsettings set \
  --resource-group optimaize-rg \
  --name $WEB_APP_NAME \
  --settings \
  AZURE_SEARCH_ENDPOINT="https://optimaize-search.search.windows.net" \
  AZURE_SEARCH_API_KEY="your-search-api-key"
```

### 3. Upload Documents and Index

```bash
# Get your app URL
APP_URL="https://$WEB_APP_NAME.azurewebsites.net"

# Upload documents (you'll need to implement file upload endpoint)
# Or use Azure Storage and configure the app to read from there

# Trigger indexing via API
curl -X POST "$APP_URL/admin/index"

# Check status
curl "$APP_URL/health"
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file for local development:

```bash
# Core settings
ENVIRONMENT=local
API_HOST=0.0.0.0
API_PORT=8000

# External services
QDRANT_URL=http://localhost:6333
ELASTICSEARCH_URL=http://localhost:9200
OLLAMA_URL=http://localhost:11434

# Optional: Azure services
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_SEARCH_ENDPOINT=
AZURE_SEARCH_API_KEY=

# Security
JWT_SECRET=your-secret-key
ADMIN_USERNAME=admin
ADMIN_PASSWORD=change-this
```

### Config File

Edit `config/config.yaml` to customize:

```yaml
# Indexing settings
indexing:
  chunk_size: 1000        # Tokens per chunk
  chunk_overlap: 200      # Overlap between chunks
  batch_size: 10          # Files to process at once

# Retrieval settings  
retrieval:
  fusion_method: "rrf"    # Reciprocal Rank Fusion
  top_k_per_source: 20    # Results from each engine
  final_top_k: 10         # Final results after fusion

# LLM settings
llm:
  default_model: "llama3"
  temperature: 0.7
  max_tokens: 2048
```

## 🤖 Teams Bot Integration

After Azure deployment is working:

### 1. Update Teams Bot Code

Your Teams bot is in the `teams-bot/` folder. Update the endpoints:

```python
# In teams-bot/app.py
OPTIMAIZE_API_URL = "https://your-app-name.azurewebsites.net"

async def handle_message(activity: Activity) -> str:
    user_message = activity.text
    
    # Call your OptimAIze API
    response = requests.get(
        f"{OPTIMAIZE_API_URL}/search",
        params={"q": user_message, "top_k": 5}
    )
    
    if response.status_code == 200:
        results = response.json()
        return format_search_results(results)
    else:
        return "Sorry, I couldn't search the documents right now."
```

### 2. Deploy Teams Bot

```bash
# Deploy the Teams bot separately or integrate into main app
cd teams-bot
az webapp create \
  --resource-group optimaize-rg \
  --plan optimaize-plan \
  --name optimaize-teams-bot \
  --runtime "PYTHON|3.11"
```

## 📊 Usage Commands

### Local Commands

```bash
# Setup and start
./startup.sh setup              # Full setup
./startup.sh start              # Start API server
./startup.sh docker             # Start with Docker services

# Document management
./startup.sh index              # Index documents
./startup.sh index --force      # Force re-index
./startup.sh status             # Show system status

# Maintenance
./startup.sh clean              # Clean up local setup
```

### CLI Commands

```bash
# Activate virtual environment first
source venv/bin/activate

# Search and ask questions
python main.py query "search term"
python main.py ask "What is the company policy?"

# Index management
python main.py index --input-dir /path/to/docs
python main.py status --json-output
python main.py reprocess path/to/file.pdf
```

### API Endpoints

```bash
# Search
GET /search?q=query&mode=hybrid&top_k=10

# Health and status
GET /health
GET /stats  
GET /status

# Admin (if implemented)
POST /admin/index
GET /admin/dashboard
```

## 🚨 Troubleshooting

### Common Issues

**Services not starting:**
```bash
# Check Docker services
docker-compose logs qdrant
docker-compose logs elasticsearch

# Restart services
docker-compose restart
```

**Import errors:**
```bash
# Reinstall dependencies
./startup.sh clean
./startup.sh setup
```

**Out of memory:**
```bash
# Reduce batch sizes in config.yaml
indexing:
  batch_size: 5
  chunk_size: 500
```

**Azure deployment issues:**
```bash
# Check Azure logs
az webapp log tail --resource-group optimaize-rg --name $WEB_APP_NAME

# Restart web app
az webapp restart --resource-group optimaize-rg --name $WEB_APP_NAME
```

### Performance Tuning

```bash
# For large document sets
export EMBEDDING_DEVICE=cuda  # If GPU available
# Increase batch sizes in config

# For limited resources  
export EMBEDDING_DEVICE=cpu
# Reduce chunk_size and batch_size
```

## 📚 Next Steps

1. **Test locally** with your documents
2. **Deploy to Azure** and verify it works
3. **Set up external services** (Qdrant, Elasticsearch)
4. **Configure Teams bot** to use your API
5. **Upload and index** your company documents
6. **Test end-to-end** workflow

## 🆘 Support

- Check logs in `logs/` directory
- Use `./startup.sh status` for health checks
- Review API docs at `/docs` endpoint
- Monitor Azure logs with `az webapp log tail`

## 🔒 Security Notes

- Change default admin credentials
- Use Azure Key Vault for secrets in production
- Configure proper CORS origins
- Enable HTTPS only in production
- Regularly update dependencies

---

### Team Contacts
- **Technical Lead**: @joaquinnsalas
- **DevOps**: @your-devops-team
- **Product**: @your-product-team

---

## 📄 License

This project is proprietary software. See [LICENSE](LICENSE) for details.

---

*Built with ❤️ by the OptimAIze team*