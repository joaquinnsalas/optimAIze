#!/usr/bin/env python3
"""CLI entrypoint for OptimAIze indexing pipeline."""

import os
import click
import json
from pathlib import Path

# Set environment variables before importing other modules
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

from src.indexing.pipeline import indexing_pipeline
from src.utils.logger import logger
from src.config.settings import config

@click.group()
def cli():
    """OptimAIze - Production-Grade RAG System"""
    pass

@cli.command()
@click.argument('question')
@click.option('--mode', '-m', default='hybrid', help='Search mode: hybrid, semantic, keyword')
@click.option('--top-k', '-k', default=5, help='Number of chunks to retrieve')
@click.option('--min-similarity', '-s', default=0.0, help='Minimum similarity threshold')
@click.option('--model', default=None, help='LLM model to use (overrides config)')
@click.option('--temperature', '-t', type=float, default=None, help='Generation temperature (0.0-1.0)')
@click.option('--max-tokens', type=int, default=None, help='Maximum tokens to generate')
@click.option('--show-sources', is_flag=True, help='Show detailed source information')
def ask(question, mode, top_k, min_similarity, model, temperature, max_tokens, show_sources):
    """Ask a question and get an AI-generated answer with citations."""
    try:
        import asyncio
        from src.llm.processor import llm_processor
        from src.llm.models import LLMQuery
        
        async def run_generation():
            llm_query = LLMQuery(
                query=question,
                mode=mode,
                top_k=top_k,
                min_similarity=min_similarity,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            response = await llm_processor.process_query(llm_query)
            return response
        
        # Run the generation
        response = asyncio.run(run_generation())
        
        # Display results
        click.echo(f"\n🤖 Question: {question}")
        click.echo("=" * 80)
        
        # Show the answer
        click.echo(f"\n📝 Answer:")
        click.echo(response.llm_answer)
        
        # Show metadata
        metadata = response.metadata
        click.echo(f"\n📊 Generation Info:")
        click.echo(f"  - Model: {metadata.get('model', 'unknown')}")
        click.echo(f"  - Search mode: {metadata.get('search_mode', mode)}")
        click.echo(f"  - Chunks used: {metadata.get('chunks_used', 0)}")
        click.echo(f"  - Total time: {metadata.get('total_time_ms', 0):.1f}ms")
        
        if metadata.get('ollama_available', True):
            click.echo(f"  - Search time: {metadata.get('search_time_ms', 0):.1f}ms")
            click.echo(f"  - Generation time: {metadata.get('generation_time_ms', 0):.1f}ms")
        else:
            click.echo(f"  - ⚠️  LLM unavailable (fallback used)")
            if metadata.get('error_message'):
                click.echo(f"  - Error: {metadata.get('error_message')}")
        
        # Show sources
        if response.sources and (show_sources or len(response.sources) <= 3):
            click.echo(f"\n📚 Sources:")
            for i, source in enumerate(response.sources, 1):
                click.echo(f"  [{i}] {source.file_name}")
                if source.page_number:
                    click.echo(f"      Page {source.page_number}, Chunk {source.chunk_index + 1}")
                else:
                    click.echo(f"      Chunk {source.chunk_index + 1}")
                click.echo(f"      Score: {source.score:.3f} ({source.source_type})")
                
                if show_sources:
                    click.echo(f"      Preview: {source.content_preview}")
                click.echo()
        elif response.sources:
            click.echo(f"\n📚 Sources: {len(response.sources)} documents (use --show-sources for details)")
        
        # Show search results if no LLM answer
        if not response.llm_answer or "LLM is currently unavailable" in response.llm_answer:
            if response.search_results:
                click.echo(f"\n🔍 Raw Search Results:")
                for i, result in enumerate(response.search_results[:3], 1):
                    click.echo(f"  {i}. {result.file_name} (Score: {result.score:.3f})")
                    preview = result.content[:150] + "..." if len(result.content) > 150 else result.content
                    click.echo(f"     {preview}")
                    click.echo()
        
    except ImportError as e:
        logger.error(f"Import error in CLI ask: {e}")
        click.echo(f"❌ LLM functionality not available: {e}")
        click.echo("   Make sure all LLM dependencies are installed")
    except Exception as e:
        logger.error(f"CLI ask failed: {e}")
        click.echo(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise click.Abort()

@cli.command()
@click.option('--force', '-f', is_flag=True, help='Force reprocessing of all files')
@click.option('--input-dir', '-i', help='Override input directory')
@click.option('--batch-size', '-b', type=int, help='Override batch size')
def index(force, input_dir, batch_size):
    """Run the indexing pipeline on documents."""
    try:
        # Override config if specified
        overrides = {}
        if input_dir:
            overrides['input_directory'] = input_dir
        if batch_size:
            overrides['batch_size'] = batch_size
            
        # Run indexing
        result = indexing_pipeline.run_pipeline(force=force, config_overrides=overrides)
        
        # Display results
        click.echo("\n" + "=" * 50)
        click.echo("INDEXING RESULTS")
        click.echo("=" * 50)
        click.echo(f"Status: {result['status']}")
        click.echo(f"Files processed: {result['files_processed']}")
        click.echo(f"Chunks created: {result['chunks_created']}")
        click.echo(f"Duration: {result['duration_seconds']:.2f} seconds")
        click.echo(f"Processing rate: {result['processing_rate']:.2f} files/second")
        
        if result['failed_files']:
            click.echo(f"\n❌ Failed files ({len(result['failed_files'])}):")
            for failed_file in result['failed_files']:
                click.echo(f"  - {failed_file}")
        
        if result['status'] == 'completed':
            click.echo("\n✅ Indexing completed successfully!")
        else:
            click.echo(f"\n⚠️  Indexing completed with status: {result['status']}")
            
    except Exception as e:
        logger.error(f"CLI indexing failed: {e}")
        click.echo(f"❌ Error: {e}")
        raise click.Abort()

@cli.command()
@click.option('--json-output', '-j', is_flag=True, help='Output as JSON')
def status(json_output):
    """Show pipeline status and statistics."""
    try:
        status_info = indexing_pipeline.get_pipeline_status()
        
        if json_output:
            click.echo(json.dumps(status_info, indent=2, default=str))
        else:
            _display_status_human_readable(status_info)
            
    except Exception as e:
        logger.error(f"CLI status check failed: {e}")
        click.echo(f"❌ Error: {e}")
        raise click.Abort()

@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
def reprocess(file_path):
    """Reprocess a single file."""
    try:
        file_path = Path(file_path)
        result = indexing_pipeline.process_single_file(file_path, force=True)
        
        if result['success']:
            click.echo(f"✅ Successfully reprocessed {file_path}")
            click.echo(f"   Created {result['chunks_created']} chunks")
        else:
            click.echo(f"❌ Failed to reprocess {file_path}")
            click.echo(f"   Error: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        logger.error(f"CLI reprocessing failed: {e}")
        click.echo(f"❌ Error: {e}")
        raise click.Abort()

@cli.command()
@click.argument('query')
@click.option('--mode', '-m', default='hybrid', help='Search mode: hybrid, semantic, keyword')
@click.option('--top-k', '-k', default=5, help='Number of results to return')
@click.option('--min-similarity', '-s', default=0.0, help='Minimum similarity threshold')
def query(query, mode, top_k, min_similarity):
    """Search documents from the command line."""
    try:
        import asyncio
        
        # Test individual imports step by step
        logger.info("Testing imports...")
        
        try:
            from src.retrieval.models import SearchResult, SearchQuery, SearchResponse
            logger.info("✅ Models imported")
        except Exception as e:
            logger.error(f"❌ Models import failed: {e}")
            raise
        
        try:
            from src.retrieval.query_processor import QueryProcessor
            logger.info("✅ QueryProcessor imported")
        except Exception as e:
            logger.error(f"❌ QueryProcessor import failed: {e}")
            raise
        
        try:
            from src.retrieval.fusion import ResultFusion
            logger.info("✅ ResultFusion imported")
        except Exception as e:
            logger.error(f"❌ ResultFusion import failed: {e}")
            raise
        
        try:
            from src.retrieval.search_engine import search_engine
            logger.info("✅ SearchEngine imported")
        except Exception as e:
            logger.error(f"❌ SearchEngine import failed: {e}")
            raise
        
        async def run_search():
            response = await search_engine.search(
                query=query,
                mode=mode,
                top_k=top_k,
                min_similarity=min_similarity
            )
            return response
        
        # Run the search
        response = asyncio.run(run_search())
        
        # Display results
        click.echo(f"\n🔍 Search Results for: '{query}'")
        click.echo(f"Mode: {response.mode} | Found: {response.total_found} | Time: {response.search_time_ms:.1f}ms")
        click.echo("=" * 80)
        
        if not response.results:
            click.echo("No results found.")
            return
        
        for i, result in enumerate(response.results, 1):
            click.echo(f"\n{i}. {result.file_name}")
            click.echo(f"   Score: {result.score:.4f} | Source: {result.source_type}")
            click.echo(f"   Chunk {result.chunk_index + 1}")
            
            # Show content preview
            content_preview = result.content[:200] + "..." if len(result.content) > 200 else result.content
            click.echo(f"   {content_preview}")
            
            # Show highlights if available
            if result.highlights:
                click.echo(f"   Highlights: {', '.join(result.highlights[:2])}")
        
        # Show fusion info for hybrid search
        if response.fusion_method:
            click.echo(f"\n📊 Fusion: {response.fusion_method}")
            if response.fusion_params:
                for key, value in response.fusion_params.items():
                    if key != "method":
                        click.echo(f"   {key}: {value}")
        
    except Exception as e:
        logger.error(f"CLI search failed: {e}")
        click.echo(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise click.Abort()

@cli.command()
def serve():
    """Start the API server."""
    try:
        logger.info("Checking FastAPI/Uvicorn availability...")
        import uvicorn
        import fastapi
        logger.info("FastAPI/Uvicorn available, importing API...")
        
        from src.retrieval.api import app
        
        logger.info("Starting OptimAIze API server...")
        
        # Get configuration
        host = os.getenv("API_HOST", "0.0.0.0")
        port = int(os.getenv("API_PORT", "8000"))
        
        click.echo(f"🚀 Starting API server at http://{host}:{port}")
        click.echo("Available endpoints:")
        click.echo("  GET  /search?q=your_query")
        click.echo("  GET  /health")
        click.echo("  GET  /stats")
        click.echo("  GET  /query-suggestions?q=query")
        click.echo("\nPress Ctrl+C to stop")
        
        uvicorn.run(app, host=host, port=port, log_level="info")
        
    except ImportError as e:
        logger.error(f"Import error starting API server: {e}")
        click.echo(f"❌ Import error: {e}")
        click.echo("Install missing dependencies with: pip install fastapi uvicorn")
    except Exception as e:
        logger.error(f"Failed to start API server: {e}")
        click.echo(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise click.Abort()

@cli.command()
def config_info():
    """Display current configuration."""
    click.echo("OptimAIze Configuration:")
    click.echo("=" * 40)
    
    click.echo(f"App:")
    click.echo(f"  - Name: {config.app.get('name')}")
    click.echo(f"  - Version: {config.app.get('version')}")
    click.echo(f"  - Log level: {config.app.get('log_level')}")
    
    click.echo(f"\nIndexing:")
    click.echo(f"  - Input directory: {config.indexing.get('input_directory')}")
    click.echo(f"  - Chunk size: {config.indexing.get('chunk_size')} tokens")
    click.echo(f"  - Chunk overlap: {config.indexing.get('chunk_overlap')} tokens")
    click.echo(f"  - Batch size: {config.indexing.get('batch_size')}")
    
    click.echo(f"\nEmbeddings:")
    click.echo(f"  - Model: {config.embeddings.get('model_name')}")
    click.echo(f"  - Dimension: {config.embeddings.get('dimension')}")
    click.echo(f"  - Device: {config.embeddings.get('device')}")
    
    click.echo(f"\nRetrieval:")
    click.echo(f"  - Fusion method: {config.retrieval.get('fusion_method')}")
    click.echo(f"  - Top-k per source: {config.retrieval.get('top_k_per_source')}")
    click.echo(f"  - Final top-k: {config.retrieval.get('final_top_k')}")
    click.echo(f"  - Min similarity: {config.retrieval.get('min_similarity_threshold')}")
    click.echo(f"  - RRF k-value: {config.retrieval.get('rrf_k')}")
    click.echo(f"  - Concurrent search: {config.retrieval.get('concurrent_search')}")
    
    click.echo(f"\nStorage:")
    click.echo(f"  - Qdrant URL: {config.qdrant.get('url')}")
    click.echo(f"  - Elasticsearch URL: {config.elasticsearch.get('url')}")
    click.echo(f"  - Database type: {config.database.get('type')}")

def _display_status_human_readable(status_info):
    """Display status in human-readable format."""
    click.echo("\n" + "=" * 50)
    click.echo("OPTIMAIZE PIPELINE STATUS") 
    click.echo("=" * 50)
    
    # Overall health
    health = status_info.get('health', {})
    overall_health = "✅ Healthy" if health.get('overall') else "❌ Unhealthy"
    click.echo(f"Overall Health: {overall_health}")
    
    if not health.get('qdrant'):
        click.echo("  - Qdrant: ❌")
    else:
        click.echo("  - Qdrant: ✅")
        
    if not health.get('elasticsearch'):
        click.echo("  - Elasticsearch: ❌")
    else:
        click.echo("  - Elasticsearch: ✅")
    
    # Database stats
    db_stats = status_info.get('database_stats', {})
    click.echo(f"\nDatabase Statistics:")
    click.echo(f"  - Total files: {db_stats.get('total_files', 0)}")
    click.echo(f"  - Completed files: {db_stats.get('completed_files', 0)}")
    click.echo(f"  - Failed files: {db_stats.get('failed_files', 0)}")
    click.echo(f"  - Processing files: {db_stats.get('processing_files', 0)}")
    click.echo(f"  - Total chunks: {db_stats.get('total_chunks', 0)}")
    
    # Qdrant stats
    qdrant_stats = status_info.get('qdrant_stats', {})
    click.echo(f"\nQdrant Vector Database:")
    click.echo(f"  - Collection: {qdrant_stats.get('collection_name', 'N/A')}")
    click.echo(f"  - Points: {qdrant_stats.get('points_count', 0)}")
    click.echo(f"  - Vector size: {qdrant_stats.get('vector_size', 0)}")
    click.echo(f"  - Distance metric: {qdrant_stats.get('distance', 'N/A')}")
    
    # Elasticsearch stats
    es_stats = status_info.get('elasticsearch_stats', {})
    click.echo(f"\nElasticsearch Keyword Index:")
    click.echo(f"  - Index: {es_stats.get('index_name', 'N/A')}")
    click.echo(f"  - Documents: {es_stats.get('document_count', 0)}")
    click.echo(f"  - Store size: {es_stats.get('store_size_bytes', 0)} bytes")
    
    # Embedding model info
    embedding_stats = status_info.get('embedding_stats', {})
    click.echo(f"\nEmbedding Model:")
    click.echo(f"  - Model: {embedding_stats.get('model_name', 'N/A')}")
    click.echo(f"  - Dimension: {embedding_stats.get('dimension', 0)}")
    click.echo(f"  - Device: {embedding_stats.get('device', 'N/A')}")

if __name__ == "__main__":
    cli()