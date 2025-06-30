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
def ask(question, mode, top_k):
    """Ask a question and get an AI-generated answer with citations."""
    try:
        import asyncio
        from azure.core.credentials import AzureKeyCredential
        from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
        from langchain.schema import SystemMessage, HumanMessage
        from src.retrieval.search_engine import search_engine
        import os
        from dotenv import load_dotenv
        
        load_dotenv()

        # Azure AI setup
        ENDPOINT = os.getenv("AZURE_INFERENCE_ENDPOINT")
        API_KEY = os.getenv("AZURE_INFERENCE_KEY") 
        CHAT_MODEL = os.getenv("AZURE_CHAT_MODEL", "gpt-4o-mini")

        if not ENDPOINT or not API_KEY:
            click.echo("❌ Missing Azure credentials. Set AZURE_INFERENCE_ENDPOINT and AZURE_INFERENCE_KEY")
            return
        
        cred = AzureKeyCredential(API_KEY)
        chat_model = AzureAIChatCompletionsModel(
            endpoint=ENDPOINT, 
            credential=cred,
            model=CHAT_MODEL, 
            temperature=0.3
        )
        
        async def run_generation():
            # Search using your existing system
            search_response = await search_engine.search(
                query=question,
                mode=mode,
                top_k=top_k
            )
            
            if not search_response.results:
                # No results - direct LLM
                resp = chat_model.invoke([
                    SystemMessage(content="You are OptimAIze, Altura Engineering's helpful assistant."),
                    HumanMessage(content=question)
                ])
                return resp.content, []
            
            # Build context from search results
            context = "\n".join([result.content for result in search_response.results[:3]])
            
            # Generate answer with context
            resp = chat_model.invoke([
                SystemMessage(content="You are OptimAIze, Altura Engineering's document assistant. Answer based on the provided context."),
                HumanMessage(content=f"Context: {context}\n\nQuestion: {question}")
            ])
            
            return resp.content, search_response.results
        
        # Run generation
        answer, sources = asyncio.run(run_generation())
        
        # Display results
        click.echo(f"\n🤖 Question: {question}")
        click.echo("=" * 80)
        click.echo(f"\n📝 Answer:")
        click.echo(answer)
        
        if sources:
            click.echo(f"\n📚 Sources:")
            for i, source in enumerate(sources[:3], 1):
                click.echo(f"  [{i}] {source.file_name} (Score: {source.score:.3f})")
                preview = source.content[:100] + "..." if len(source.content) > 100 else source.content
                click.echo(f"      {preview}")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}")

@cli.command()
def webapp():
    """Start the Flask web interface."""
    try:
        from flask import Flask, request, jsonify, render_template
        import asyncio
        from azure.core.credentials import AzureKeyCredential
        from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
        from langchain.schema import SystemMessage, HumanMessage
        from src.retrieval.search_engine import search_engine
        import os
        from dotenv import load_dotenv
        
        load_dotenv()

        # Azure AI setup
        ENDPOINT = os.getenv("AZURE_INFERENCE_ENDPOINT")
        API_KEY = os.getenv("AZURE_INFERENCE_KEY")
        CHAT_MODEL = os.getenv("AZURE_CHAT_MODEL", "gpt-4o-mini")

        if not ENDPOINT or not API_KEY:
            click.echo("❌ Missing Azure credentials. Set AZURE_INFERENCE_ENDPOINT and AZURE_INFERENCE_KEY")
            return
        
        cred = AzureKeyCredential(API_KEY)
        chat_model = AzureAIChatCompletionsModel(
            endpoint=ENDPOINT,
            credential=cred, 
            model=CHAT_MODEL,
            temperature=0.3
        )
        
        app = Flask(__name__)
        
        @app.route("/")
        def index():
            """Serve the main web interface."""
            return render_template('index.html')
        
        @app.route("/api/chat", methods=["POST"])
        def chat():
            """Handle chat API requests."""
            try:
                data = request.get_json()
                question = data.get("query", "").strip()
                
                if not question:
                    return jsonify(error="No question provided"), 400
                
                # Make this sync by using asyncio.run
                import asyncio
                
                def process():
                    async def async_process():
                        try:
                            search_response = await search_engine.search(
                                query=question, 
                                mode="hybrid", 
                                top_k=8
                            )
                        except Exception as e:
                            logger.error(f"Search failed: {e}")
                            # If search fails, use direct LLM
                            search_response = type('obj', (object,), {'results': []})()
                        
                        if not search_response.results:
                            resp = chat_model.invoke([
                                SystemMessage(content="You are OptimAIze, Altura Engineering's helpful assistant."),
                                HumanMessage(content=question)
                            ])
                            return resp.content, []
                        
                        # Build context from search results with better handling
                        context_parts = []
                        total_chars = 0
                        max_chars = 4000
                        
                        for result in search_response.results[:5]:
                            content = result.content
                            if len(content) > 800:
                                content = content[:800] + "..."
                                
                            if total_chars + len(content) < max_chars:
                                context_parts.append(f"Source: {result.file_name}\n{content}")
                                total_chars += len(content)
                            else:
                                break
                        
                        context = "\n\n---\n\n".join(context_parts)
                        
                        resp = chat_model.invoke([
                            SystemMessage(content="You are OptimAIze, Altura Engineering's document assistant. Answer based ONLY on the provided context. If the context contains relevant information, use it. If not, clearly state that the information is not found in the provided documents."),
                            HumanMessage(content=f"Context from company documents:\n\n{context}\n\nQuestion: {question}")
                        ])
                        
                        sources = [f"{r.file_name} (Score: {r.score:.3f})" for r in search_response.results[:3]]
                        return resp.content, sources
                    
                    return asyncio.run(async_process())
                
                answer, sources = process()
                return jsonify(answer=answer, sources=sources)
                
            except Exception as e:
                logger.error(f"Chat API error: {e}")
                return jsonify(error=str(e)), 500
        
        click.echo("🚀 Starting OptimAIze Web Interface at http://localhost:5001")
        click.echo("✨ Enhanced UI with loading indicators and suggested questions")
        app.run(host="0.0.0.0", port=5001, debug=True)
        
    except Exception as e:
        click.echo(f"❌ Error: {e}")

@cli.command()
@click.option('--force', '-f', is_flag=True, help='Force reprocessing of all files')
@click.option('--input-dir', '-i', help='Override input directory')
@click.option('--batch-size', '-b', type=int, help='Override batch size')
def index(force, input_dir, batch_size):
    """Run the indexing pipeline on documents."""
    try:
        # Apply config overrides if specified
        if input_dir:
            indexing_pipeline.input_directory = Path(input_dir)
            logger.info(f"Using custom input directory: {input_dir}")
        
        if batch_size:
            indexing_pipeline.batch_size = batch_size
            logger.info(f"Using custom batch size: {batch_size}")
            
        # Run indexing with the correct method name and parameter
        result = indexing_pipeline.run_full_pipeline(force_reprocess=force)
        
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

if __name__ == "__main__":
    cli()