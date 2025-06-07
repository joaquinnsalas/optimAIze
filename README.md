# OptimAIze - Production-Grade RAG System

OptimAIze is a robust, enterprise-ready Retrieval-Augmented Generation (RAG) system that combines semantic vector search with keyword search for optimal document retrieval and LLM-powered synthesis.

## 🚀 Features

- **Hybrid Search**: Combines Qdrant vector search with Elasticsearch keyword search
- **Multi-Format Support**: PDF (with OCR), DOCX, PPTX, TXT, MD, XLSX
- **Production Ready**: Dockerized with proper logging, error handling, and monitoring
- **Scalable Architecture**: Modular design with clear separation of concerns
- **Advanced Chunking**: Sentence-aware text splitting with token optimization
- **Embeddings**: Uses nomic-embed-text-v1 for high-quality vector representations

## 📁 Project Structure

```
optimaize-indexer/
├── src/
│   ├── config/          # Configuration management
│   ├── indexing/        # Document processing pipeline
│   ├── storage/         # Database clients (Qdrant, Elasticsearch, SQLite)
│   └── utils/           # Utilities and logging
├── data/
│   ├── documents/       # Input documents
│   ├── logs/           # Application logs
│   └── processed/      # Processing metadata
├── config/             # Configuration files
├── docker-compose.yml  # Container orchestration
├── Dockerfile         # Application container
├── main.py           # CLI entrypoint
└── requirements.txt  # Python dependencies
```

## 🛠 Installation

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- At least 4GB RAM for embeddings model

### Quick Start

1. **Clone and setup:**
```bash
git clone <repository>
cd optimaize-indexer
```

2. **Start infrastructure:**
```bash
# Start Qdrant and Elasticsearch
docker-compose up -d qdrant elasticsearch

# Wait for services to be healthy
docker-compose ps
```

3. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure the system:**
```bash
# Edit config/config.yaml as needed
cp config/config.yaml config/config.yaml.local
```

5. **Add documents and run indexing:**
```bash
# Add your documents to data/documents/
mkdir -p data/documents
cp /path/to/your/docs/* data/documents/

# Run the indexing pipeline
python main.py index
```

## 📋 CLI Usage

### Index Documents
```bash
# Index all documents in the configured directory
python main.py index

# Force reprocessing of all documents
python main.py index --force

# Use custom input directory
python main.py index --input-dir /path/to/docs

# Process with custom batch size
python main.py index --batch-size 50
```

### Check Status
```bash
# Human-readable status
python main.py status

# JSON output for programmatic use
python main.py status --json
```

### Reprocess Single File
```bash
python main.py reprocess data/documents/important.pdf
```

### View Configuration
```bash
python main.py config-info
```

## ⚙️ Configuration

The system is configured via `config/config.yaml`. Key settings:

### Indexing Settings
```yaml
indexing:
  input_directory: "data/documents"
  supported_extensions: [".pdf", ".docx", ".pptx", ".txt", ".md", ".xlsx"]
  chunk_size: 512          # tokens
  chunk_overlap: 50        # tokens
  ocr_dpi: 300            # for PDF OCR
  batch_size: 100         # files per batch
```

### Embeddings
```yaml
embeddings:
  model_name: "nomic-ai/nomic-embed-text-v1"
  dimension: 768
  device: "cpu"  # or "cuda"
```

### Storage
```yaml
qdrant:
  url: "http://localhost:6333"
  collection_name: "optimaize_documents"

elasticsearch:
  url: "http://localhost:9200"
  index_name: "optimaize_keywords"

database:
  type: "sqlite"
  sqlite_path: "data/metadata.db"
```

## 🐳 Docker Deployment

### Development
```bash
# Start just the databases
docker-compose up -d qdrant elasticsearch

# Run indexing locally
python main.py index
```

### Full Deployment
```bash
# Build and start everything
docker-compose --profile app up -d

# Check status
docker-compose ps
docker-compose logs optimaize-app
```

## 📊 Monitoring

### Health Checks
```bash
# Check overall system health
python main.py status

# Individual service health
curl http://localhost:6333/health      # Qdrant
curl http://localhost:9200/_cluster/health  # Elasticsearch
```

### Logs
```bash
# Application logs
tail -f data/logs/optimaize.log

# Error logs
tail -f data/logs/errors.log

# Docker logs
docker-compose logs -f optimaize-app
```

## 🔧 Development

### Adding New File Types

1. Extend `src/indexing/file_loader.py`:
```python
def _load_new_format(self, file_path: Path) -> Dict[str, Any]:
    # Implementation here
    pass
```

2. Update supported extensions in config:
```yaml
indexing:
  supported_extensions: [".pdf", ".docx", ".new_format"]
```

### Custom Chunking Strategies

Modify `src/indexing/chunker.py` to implement domain-specific chunking logic.

### Environment Variables

Override config with environment variables:
- `QDRANT_URL`
- `ELASTICSEARCH_URL`
- `DATABASE_TYPE`
- `POSTGRESQL_URL`
- `EMBEDDING_DEVICE`

## 📈 Performance Tips

1. **GPU Acceleration**: Set `EMBEDDING_DEVICE=cuda` for faster embeddings
2. **Batch Size**: Increase batch size for faster processing of many small files
3. **Memory**: Ensure sufficient RAM for the embedding model (~2GB)
4. **Storage**: Use SSD storage for better database performance

## 🚨 Troubleshooting

### Common Issues

**Qdrant Connection Error:**
```bash
# Check if Qdrant is running
docker-compose ps qdrant
curl http://localhost:6333/health
```

**Elasticsearch Connection Error:**
```bash
# Check Elasticsearch status
docker-compose ps elasticsearch
curl http://localhost:9200/_cluster/health
```

**OCR Issues:**
```bash
# Verify tesseract installation
tesseract --version
```

**Memory Issues:**
- Reduce batch size in config
- Use CPU instead of GPU for embeddings
- Increase Docker memory limits

### Reset Everything
```bash
# Stop services
docker-compose down -v

# Remove data
rm -rf data/metadata.db data/logs/*

# Restart
docker-compose up -d qdrant elasticsearch
```

## 📝 Next Steps

This completes **Chunk 1: Indexing Pipeline**. The system now supports:

✅ Recursive file loading with duplicate detection  
✅ Multi-format document processing with OCR  
✅ Sentence-aware chunking with token counting  
✅ Vector embeddings with nomic-embed-text-v1  
✅ Qdrant vector storage  
✅ Elasticsearch keyword indexing  
✅ SQLite metadata tracking  
✅ CLI interface with comprehensive commands  
✅ Docker deployment  
✅ Production logging and error handling  

Ready for **Chunk 2: Retrieval + Hybrid Search**? 🚀