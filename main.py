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
@click.version_option(version=config.app.get("version", "1.0.0"))
def cli():
    """OptimAIze - Production-grade RAG system with hybrid search."""
    pass

@cli.command()
@click.option('--force', '-f', is_flag=True, help='Force reprocessing of all files')
@click.option('--input-dir', '-i', type=click.Path(exists=True, path_type=Path), 
              help='Input directory (overrides config)')
@click.option('--batch-size', '-b', type=int, help='Batch size for processing')
def index(force, input_dir, batch_size):
    """Run the indexing pipeline to process documents."""
    try:
        # Override config if provided
        if input_dir:
            config._config["indexing"]["input_directory"] = str(input_dir)
        if batch_size:
            config._config["indexing"]["batch_size"] = batch_size
        
        logger.info(f"Starting indexing pipeline (force={force})")
        
        # Run the pipeline
        result = indexing_pipeline.run_full_pipeline(force_reprocess=force)
        
        # Display results
        click.echo("\n" + "="*50)
        click.echo("INDEXING RESULTS")
        click.echo("="*50)
        click.echo(f"Status: {result['status']}")
        click.echo(f"Files processed: {result['files_processed']}")
        click.echo(f"Chunks created: {result['chunks_created']}")
        click.echo(f"Duration: {result['duration_seconds']:.2f} seconds")
        click.echo(f"Processing rate: {result['processing_rate']:.2f} files/second")
        
        if result.get('failed_files'):
            click.echo(f"\nFailed files ({len(result['failed_files'])}):")
            for failed in result['failed_files']:
                click.echo(f"  - {failed['file']}: {failed['error']}")
        
        if result['status'] == 'completed':
            click.echo("\n✅ Indexing completed successfully!")
        else:
            click.echo(f"\n❌ Indexing failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        logger.error(f"CLI indexing failed: {e}")
        click.echo(f"❌ Error: {e}")
        raise click.Abort()

@cli.command()
@click.argument('file_path', type=click.Path(exists=True, path_type=Path))
def reprocess(file_path):
    """Reprocess a specific file."""
    try:
        logger.info(f"Reprocessing file: {file_path}")
        
        result = indexing_pipeline.reprocess_file(file_path)
        
        if result['success']:
            click.echo(f"✅ Successfully reprocessed {file_path}")
            click.echo(f"   Chunks created: {result['chunks_created']}")
        else:
            click.echo(f"❌ Failed to reprocess {file_path}")
            click.echo(f"   Error: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        logger.error(f"CLI reprocessing failed: {e}")
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

def _display_status_human_readable(status_info):
    """Display status in human-readable format."""
    click.echo("\n" + "="*50)
    click.echo("OPTIMAIZE PIPELINE STATUS")
    click.echo("="*50)
    
    # Health status
    health = status_info.get('health_status', {})
    overall_health = health.get('overall', False)
    status_icon = "✅" if overall_health else "❌"
    click.echo(f"Overall Health: {status_icon} {'Healthy' if overall_health else 'Unhealthy'}")
    click.echo(f"  - Qdrant: {'✅' if health.get('qdrant') else '❌'}")
    click.echo(f"  - Elasticsearch: {'✅' if health.get('elasticsearch') else '❌'}")
    
    # Database stats
    db_stats = status_info.get('database_stats', {})
    if db_stats:
        click.echo(f"\nDatabase Statistics:")
        click.echo(f"  - Total files: {db_stats.get('total_files', 0)}")
        click.echo(f"  - Completed files: {db_stats.get('completed_files', 0)}")
        click.echo(f"  - Failed files: {db_stats.get('failed_files', 0)}")
        click.echo(f"  - Processing files: {db_stats.get('processing_files', 0)}")
        click.echo(f"  - Total chunks: {db_stats.get('total_chunks', 0)}")
    
    # Qdrant info
    qdrant_info = status_info.get('qdrant_info', {})
    if qdrant_info:
        click.echo(f"\nQdrant Vector Database:")
        click.echo(f"  - Collection: {qdrant_info.get('name', 'N/A')}")
        click.echo(f"  - Points: {qdrant_info.get('points_count', 0)}")
        click.echo(f"  - Vector size: {qdrant_info.get('vector_size', 0)}")
        click.echo(f"  - Distance metric: {qdrant_info.get('distance', 'N/A')}")
    
    # Elasticsearch info
    es_info = status_info.get('elasticsearch_info', {})
    if es_info:
        click.echo(f"\nElasticsearch Keyword Index:")
        click.echo(f"  - Index: {es_info.get('index_name', 'N/A')}")
        click.echo(f"  - Documents: {es_info.get('document_count', 0)}")
        click.echo(f"  - Store size: {es_info.get('store_size', 0)} bytes")
    
    # Embedder info
    embedder_info = status_info.get('embedder_info', {})
    if embedder_info:
        click.echo(f"\nEmbedding Model:")
        click.echo(f"  - Model: {embedder_info.get('model_name', 'N/A')}")
        click.echo(f"  - Dimension: {embedder_info.get('dimension', 0)}")
        click.echo(f"  - Device: {embedder_info.get('device', 'N/A')}")

@cli.command()
def config_info():
    """Show current configuration."""
    click.echo("\n" + "="*50)
    click.echo("OPTIMAIZE CONFIGURATION")
    click.echo("="*50)
    
    click.echo(f"App: {config.app.get('name')} v{config.app.get('version')}")
    click.echo(f"Log level: {config.app.get('log_level')}")
    
    click.echo(f"\nIndexing:")
    click.echo(f"  - Input directory: {config.indexing.get('input_directory')}")
    click.echo(f"  - Supported extensions: {config.indexing.get('supported_extensions')}")
    click.echo(f"  - Chunk size: {config.indexing.get('chunk_size')} tokens")
    click.echo(f"  - Chunk overlap: {config.indexing.get('chunk_overlap')} tokens")
    click.echo(f"  - Batch size: {config.indexing.get('batch_size')}")
    
    click.echo(f"\nEmbeddings:")
    click.echo(f"  - Model: {config.embeddings.get('model_name')}")
    click.echo(f"  - Dimension: {config.embeddings.get('dimension')}")
    click.echo(f"  - Device: {config.embeddings.get('device')}")
    
    click.echo(f"\nStorage:")
    click.echo(f"  - Qdrant URL: {config.qdrant.get('url')}")
    click.echo(f"  - Elasticsearch URL: {config.elasticsearch.get('url')}")
    click.echo(f"  - Database type: {config.database.get('type')}")

if __name__ == '__main__':
    cli()