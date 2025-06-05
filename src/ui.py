import gradio as gr
import logging
from typing import List, Dict, Tuple
import json

from search import HybridSearcher

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global searcher instance
searcher = None

def initialize_searcher():
    """Initialize the search system"""
    global searcher
    try:
        if searcher is None:
            logger.info("🔄 Initializing search system...")
            searcher = HybridSearcher()
            logger.info("✅ Search system ready")
        return True, "Search system initialized successfully"
    except Exception as e:
        logger.error(f"Failed to initialize search system: {e}")
        return False, f"Failed to initialize: {str(e)}"

def search_documents(query: str, top_k: int = 10, show_scores: bool = True) -> Tuple[str, str]:
    """
    Search documents and return formatted results
    """
    try:
        # Initialize searcher if needed
        success, message = initialize_searcher()
        if not success:
            return f"❌ **Error**: {message}", ""
        
        if not query.strip():
            return "⚠️ **Warning**: Please enter a search query", ""
        
        logger.info(f"Searching for: '{query}'")
        
        # Perform search
        results = searcher.search(query, top_k)
        
        if not results:
            return f"🔍 No results found for query: **{query}**", ""
        
        # Format results
        formatted_results = format_search_results(results, query, show_scores)
        
        # Create summary
        summary = f"📊 **Search Summary**\n"
        summary += f"- Query: **{query}**\n"
        summary += f"- Results: **{len(results)}** documents found\n"
        summary += f"- Sources: {get_source_breakdown(results)}\n\n"
        
        return formatted_results, summary
        
    except Exception as e:
        error_msg = f"❌ **Search Error**: {str(e)}"
        logger.error(f"Search failed: {e}")
        return error_msg, ""

def format_search_results(results: List[Dict], query: str, show_scores: bool = True) -> str:
    """Format search results for display"""
    formatted = f"# 🔍 Search Results for: *{query}*\n\n"
    
    for i, result in enumerate(results, 1):
        # Header with file info
        file_name = result.get('file_name', 'Unknown File')
        category = result.get('category', 'Unknown')
        
        formatted += f"## 📄 Result {i}: {file_name}\n"
        formatted += f"**Category**: {category}\n"
        
        # Scores (if enabled)
        if show_scores:
            combined_score = result.get('combined_score', 0)
            semantic_score = result.get('semantic_score', 0)
            keyword_score = result.get('keyword_score', 0)
            source = result.get('source', 'hybrid')
            
            formatted += f"**Relevance Score**: {combined_score:.4f} "
            if semantic_score:
                formatted += f"(Semantic: {semantic_score:.3f}) "
            if keyword_score:
                formatted += f"(Keyword: {keyword_score:.3f}) "
            formatted += f"[{source.title()}]\n"
        
        # Content preview
        chunk_text = result.get('chunk_text', '').strip()
        if len(chunk_text) > 300:
            preview = chunk_text[:300] + "..."
        else:
            preview = chunk_text
        
        # Highlight query terms (simple highlighting)
        highlighted_preview = highlight_query_terms(preview, query)
        
        formatted += f"\n**Content Preview**:\n{highlighted_preview}\n"
        
        # File path
        file_path = result.get('file_path', '')
        if file_path:
            formatted += f"\n*File Path*: `{file_path}`\n"
        
        formatted += "\n---\n\n"
    
    return formatted

def highlight_query_terms(text: str, query: str) -> str:
    """Simple highlighting of query terms"""
    words = query.lower().split()
    highlighted = text
    
    for word in words:
        if len(word) > 2:  # Only highlight words longer than 2 characters
            # Simple case-insensitive highlighting
            import re
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            highlighted = pattern.sub(f"**{word.upper()}**", highlighted)
    
    return highlighted

def get_source_breakdown(results: List[Dict]) -> str:
    """Get breakdown of result sources"""
    semantic_count = sum(1 for r in results if r.get('semantic_score', 0) > 0)
    keyword_count = sum(1 for r in results if r.get('keyword_score', 0) > 0)
    hybrid_count = sum(1 for r in results if r.get('semantic_score', 0) > 0 and r.get('keyword_score', 0) > 0)
    
    return f"Semantic: {semantic_count}, Keyword: {keyword_count}, Hybrid: {hybrid_count}"

def get_system_stats() -> str:
    """Get system statistics"""
    try:
        success, message = initialize_searcher()
        if not success:
            return f"❌ Error: {message}"
        
        # Get stats from database
        cursor = searcher.conn.cursor()
        doc_count = cursor.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
        chunk_count = cursor.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
        
        # Get sample categories
        categories = cursor.execute("""
            SELECT category, COUNT(*) as count 
            FROM documents 
            GROUP BY category 
            ORDER BY count DESC 
            LIMIT 5
        """).fetchall()
        
        stats = f"📊 **System Statistics**\n\n"
        stats += f"- **Total Documents**: {doc_count:,}\n"
        stats += f"- **Total Chunks**: {chunk_count:,}\n"
        stats += f"- **Average Chunks per Document**: {chunk_count/doc_count:.1f}\n\n"
        
        if categories:
            stats += "**Top Document Categories**:\n"
            for category, count in categories:
                stats += f"- {category}: {count} documents\n"
        
        return stats
        
    except Exception as e:
        return f"❌ Failed to get statistics: {str(e)}"

def test_search_system() -> str:
    """Test the search system with sample queries"""
    try:
        success, message = initialize_searcher()
        if not success:
            return f"❌ Test failed: {message}"
        
        test_queries = ["engineering", "project", "design", "analysis"]
        results_summary = "🧪 **System Test Results**\n\n"
        
        for query in test_queries:
            try:
                results = searcher.search(query, top_k=3)
                results_summary += f"- Query: **{query}** → {len(results)} results\n"
            except Exception as e:
                results_summary += f"- Query: **{query}** → ❌ Error: {str(e)}\n"
        
        results_summary += "\n✅ System test completed!"
        return results_summary
        
    except Exception as e:
        return f"❌ Test failed: {str(e)}"

# Create Gradio interface
def create_interface():
    """Create and configure the Gradio interface"""
    
    with gr.Blocks(
        title="OptimAIze Search",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px;
            margin: auto;
        }
        """
    ) as interface:
        
        gr.Markdown("""
        # 🔍 OptimAIze Search
        ### Hybrid Semantic + Keyword Search for Your Documents
        
        This system combines semantic understanding with traditional keyword matching 
        to find the most relevant content from your indexed documents.
        """)
        
        with gr.Tab("🔍 Search"):
            with gr.Row():
                with gr.Column(scale=3):
                    query_input = gr.Textbox(
                        label="Search Query",
                        placeholder="Enter your search query (e.g., 'circuit design', 'project analysis')",
                        lines=2
                    )
                    
                    with gr.Row():
                        top_k_slider = gr.Slider(
                            minimum=1,
                            maximum=20,
                            value=10,
                            step=1,
                            label="Number of Results"
                        )
                        
                        show_scores_checkbox = gr.Checkbox(
                            label="Show Relevance Scores",
                            value=True
                        )
                    
                    search_button = gr.Button("🔍 Search", variant="primary", scale=1)
                
                with gr.Column(scale=1):
                    summary_output = gr.Markdown(label="Search Summary")
            
            results_output = gr.Markdown(label="Search Results")
            
            # Example queries
            gr.Markdown("### 💡 Example Queries")
            with gr.Row():
                example_queries = [
                    "engineering project design",
                    "circuit analysis report",
                    "programming assignment",
                    "lab experiment results"
                ]
                
                for query in example_queries:
                    gr.Button(query, scale=1).click(
                        fn=lambda q=query: q,
                        outputs=query_input
                    )
        
        with gr.Tab("📊 System Info"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### System Statistics")
                    stats_button = gr.Button("📊 Get Statistics", variant="secondary")
                    stats_output = gr.Markdown()
                
                with gr.Column():
                    gr.Markdown("### System Test")
                    test_button = gr.Button("🧪 Test Search System", variant="secondary")
                    test_output = gr.Markdown()
        
        # Event handlers
        search_button.click(
            fn=search_documents,
            inputs=[query_input, top_k_slider, show_scores_checkbox],
            outputs=[results_output, summary_output]
        )
        
        # Allow Enter key to trigger search
        query_input.submit(
            fn=search_documents,
            inputs=[query_input, top_k_slider, show_scores_checkbox],
            outputs=[results_output, summary_output]
        )
        
        stats_button.click(
            fn=get_system_stats,
            outputs=stats_output
        )
        
        test_button.click(
            fn=test_search_system,
            outputs=test_output
        )
    
    return interface

if __name__ == "__main__":
    print("🚀 Starting OptimAIze Search UI...")
    print("🌐 Web interface will open automatically")
    print("📱 Access from other devices at: http://YOUR_IP:7860")
    
    interface = create_interface()
    interface.launch(
        server_name="0.0.0.0",  # Allow external access
        server_port=7860,
        share=False,  # Set to True to create public link
        debug=True
    )