import gradio as gr
import logging
from typing import List, Dict, Tuple, Optional
import json
import requests
from datetime import datetime

from search import HybridSearcher, run_system_diagnostics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global searcher instance
searcher = None

# API endpoint (if using API mode)
API_URL = "http://localhost:8000"
USE_API = False  # Set to True to use API instead of direct search

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

def search_documents(query: str, top_k: int = 10, context: str = "auto", show_scores: bool = True) -> Tuple[str, str, str]:
    """
    Search documents and return formatted results
    """
    try:
        if USE_API:
            # Use API endpoint
            response = requests.post(
                f"{API_URL}/search",
                json={
                    "query": query,
                    "top_k": top_k,
                    "context": context if context != "auto" else None
                }
            )
            if response.status_code == 200:
                data = response.json()
                results = data['results']
                detected_context = data.get('detected_context', 'general')
            else:
                return f"❌ **API Error**: {response.status_code}", "", ""
        else:
            # Use direct search
            success, message = initialize_searcher()
            if not success:
                return f"❌ **Error**: {message}", "", ""
            
            if not query.strip():
                return "⚠️ **Warning**: Please enter a search query", "", ""
            
            logger.info(f"Searching for: '{query}' with context: {context}")
            
            # Perform search
            results = searcher.search(
                query, 
                top_k,
                context=context if context != "auto" else None
            )
            detected_context = results[0].get('context', 'general') if results else 'general'
        
        if not results:
            suggestions = get_query_suggestions(query)
            no_results_msg = f"🔍 No results found for query: **{query}**\n\n"
            no_results_msg += "**Try these suggestions:**\n"
            for suggestion in suggestions:
                no_results_msg += f"- {suggestion}\n"
            return no_results_msg, "", f"Context: {detected_context}"
        
        # Format results
        formatted_results = format_search_results(results, query, show_scores)
        
        # Create summary
        summary = f"📊 **Search Summary**\n"
        summary += f"- Query: **{query}**\n"
        summary += f"- Context: **{detected_context}**\n"
        summary += f"- Results: **{len(results)}** documents found\n"
        summary += f"- Sources: {get_source_breakdown(results)}\n"
        
        # Context info
        context_info = f"🎯 **Detected Context**: {detected_context}\n"
        if detected_context == 'hr':
            context_info += "Found HR/Employee-related content"
        elif detected_context == 'technical':
            context_info += "Found Technical/Engineering content"
        elif detected_context == 'safety':
            context_info += "Found Safety-related content"
        
        return formatted_results, summary, context_info
        
    except Exception as e:
        error_msg = f"❌ **Search Error**: {str(e)}"
        logger.error(f"Search failed: {e}")
        return error_msg, "", ""

def get_query_suggestions(query: str) -> List[str]:
    """Get query suggestions based on the failed query"""
    suggestions = []
    
    # Common query patterns
    if "pto" in query.lower() or "vacation" in query.lower():
        suggestions.extend(["employee benefits", "time off policy", "leave policy"])
    elif "safety" in query.lower():
        suggestions.extend(["safety procedures", "PPE requirements", "hazard assessment"])
    elif "design" in query.lower():
        suggestions.extend(["engineering standards", "specifications", "technical requirements"])
    else:
        suggestions.extend(["employee handbook", "company policies", "procedures"])
    
    return suggestions[:3]

def format_search_results(results: List[Dict], query: str, show_scores: bool = True) -> str:
    """Format search results for display"""
    formatted = f"# 🔍 Search Results for: *{query}*\n\n"
    
    for i, result in enumerate(results, 1):
        # Header with file info
        file_name = result.get('file_name', 'Unknown File')
        category = result.get('category', 'Unknown')
        chunk_type = result.get('chunk_type', 'unknown')
        
        formatted += f"## 📄 Result {i}: {file_name}\n"
        formatted += f"**Category**: {category} | **Chunk Type**: {chunk_type}\n"
        
        # Context and scores
        if show_scores:
            combined_score = result.get('combined_score', 0)
            semantic_score = result.get('semantic_score', 0)
            keyword_score = result.get('keyword_score', 0)
            
            formatted += f"**Relevance Score**: {combined_score:.4f} "
            if semantic_score:
                formatted += f"(Semantic: {semantic_score:.3f}) "
            if keyword_score:
                formatted += f"(Keyword: {keyword_score:.3f}) "
            formatted += "\n"
        
        # Show snippet if available, otherwise show chunk preview
        if result.get('snippet'):
            formatted += f"\n**Relevant Section**:\n{result['snippet']}\n"
        else:
            chunk_text = result.get('chunk_text', '').strip()
            if len(chunk_text) > 300:
                preview = chunk_text[:300] + "..."
            else:
                preview = chunk_text
            
            # Highlight query terms
            highlighted_preview = highlight_query_terms(preview, query)
            formatted += f"\n**Content Preview**:\n{highlighted_preview}\n"
        
        # File path (shortened)
        file_path = result.get('file_path', '')
        if file_path:
            short_path = '/'.join(file_path.split('/')[-3:]) if '/' in file_path else file_path
            formatted += f"\n*Source*: `.../{short_path}`\n"
        
        formatted += "\n---\n\n"
    
    return formatted

def highlight_query_terms(text: str, query: str) -> str:
    """Highlight query terms in text"""
    words = query.lower().split()
    highlighted = text
    
    for word in words:
        if len(word) > 2:  # Only highlight meaningful words
            import re
            pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
            highlighted = pattern.sub(f"**{word.upper()}**", highlighted)
    
    return highlighted

def get_source_breakdown(results: List[Dict]) -> str:
    """Get breakdown of result sources"""
    semantic_count = sum(1 for r in results if r.get('semantic_score', 0) > 0)
    keyword_count = sum(1 for r in results if r.get('keyword_score', 0) > 0)
    hybrid_count = sum(1 for r in results if r.get('semantic_score', 0) > 0 and r.get('keyword_score', 0) > 0)
    
    return f"Semantic: {semantic_count}, Keyword: {keyword_count}, Hybrid: {hybrid_count}"

def get_system_stats() -> str:
    """Get enhanced system statistics"""
    try:
        if USE_API:
            response = requests.get(f"{API_URL}/stats")
            if response.status_code == 200:
                stats_data = response.json()
            else:
                return f"❌ Failed to get statistics from API"
        else:
            success, message = initialize_searcher()
            if not success:
                return f"❌ Error: {message}"
            
            stats_data = searcher.get_search_analytics()
        
        stats = f"📊 **System Statistics**\n\n"
        stats += f"**Document Overview:**\n"
        stats += f"- Total Documents: **{stats_data.get('total_documents', 0):,}**\n"
        stats += f"- Total Chunks: **{stats_data.get('total_chunks', 0):,}**\n"
        stats += f"- Avg Chunks/Doc: **{stats_data.get('avg_chunks_per_doc', 0):.1f}**\n\n"
        
        if 'document_types' in stats_data:
            stats += "**Document Types:**\n"
            for doc_type, count in stats_data['document_types'].items():
                stats += f"- {doc_type}: {count} documents\n"
            stats += "\n"
        
        if 'categories' in stats_data:
            stats += "**Categories:**\n"
            for category, count in sorted(stats_data['categories'].items(), key=lambda x: x[1], reverse=True):
                stats += f"- {category}: {count} documents\n"
        
        return stats
        
    except Exception as e:
        return f"❌ Failed to get statistics: {str(e)}"

def run_diagnostics() -> str:
    """Run comprehensive system diagnostics"""
    try:
        if USE_API:
            response = requests.get(f"{API_URL}/diagnostics")
            if response.status_code == 200:
                diagnostics = response.json()
            else:
                return f"❌ Failed to get diagnostics from API"
        else:
            diagnostics = run_system_diagnostics(top_k=5)
        
        report = f"🔍 **System Diagnostics Report**\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # System Status
        report += f"**System Status**: {diagnostics.get('status', 'unknown').upper()}\n\n"
        
        # Analytics Summary
        if 'analytics' in diagnostics:
            analytics = diagnostics['analytics']
            report += "**Corpus Overview:**\n"
            report += f"- Documents: {analytics.get('total_documents', 0)}\n"
            report += f"- Chunks: {analytics.get('total_chunks', 0)}\n"
            report += f"- Categories: {len(analytics.get('categories', {}))}\n\n"
        
        # Search Functionality
        report += f"**Search Functional**: {'✅ Yes' if diagnostics.get('search_functional', False) else '❌ No'}\n\n"
        
        # Sample Query Results
        if 'sample_queries' in diagnostics and diagnostics['sample_queries']:
            report += "**Sample Query Performance:**\n\n"
            
            working_queries = []
            failing_queries = []
            
            for query_info in diagnostics['sample_queries']:
                if query_info['validation']['has_results']:
                    working_queries.append(query_info)
                else:
                    failing_queries.append(query_info)
            
            if working_queries:
                report += f"✅ **Working Queries ({len(working_queries)}):**\n"
                for q in working_queries[:3]:
                    report += f"- '{q['query']}' → {q['validation']['results_found']} results\n"
                report += "\n"
            
            if failing_queries:
                report += f"⚠️ **Queries with No Results ({len(failing_queries)}):**\n"
                for q in failing_queries[:3]:
                    report += f"- '{q['query']}' ({q['type']})\n"
                report += "\n"
        
        # Recommendations
        report += "**Recommendations:**\n"
        if diagnostics.get('status') == 'healthy':
            if not diagnostics.get('search_functional', False):
                report += "- ⚠️ Search returning no results - check if documents are properly indexed\n"
                report += "- ⚠️ Try re-indexing with: `python src/indexer.py`\n"
            else:
                report += "- ✅ System is functioning normally\n"
        else:
            report += "- ❌ System unhealthy - check error logs\n"
        
        return report
        
    except Exception as e:
        return f"❌ Diagnostics failed: {str(e)}"

def get_example_queries() -> Dict[str, List[str]]:
    """Get context-specific example queries"""
    return {
        "auto": ["Let the system detect context automatically"],
        "hr": [
            "How many days of PTO do I get?",
            "What is the remote work policy?",
            "Employee benefits overview"
        ],
        "technical": [
            "Concrete slab design specifications",
            "Safety factors for structural steel",
            "Engineering design standards"
        ],
        "safety": [
            "Confined space entry procedures",
            "PPE requirements",
            "Emergency response procedures"
        ],
        "general": [
            "Company policies",
            "Project documentation",
            "Standard procedures"
        ]
    }

# Create enhanced Gradio interface
def create_interface():
    """Create and configure the enhanced Gradio interface"""
    
    with gr.Blocks(
        title="OptimAIze Search - Enterprise Edition",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1400px;
            margin: auto;
        }
        .search-box {
            font-size: 16px;
        }
        """
    ) as interface:
        
        gr.Markdown("""
        # 🔍 OptimAIze Search - Enterprise Edition
        ### Private, Intelligent Search for Your Confidential Documents
        
        **Features**: Context-aware search • Semantic understanding • Result snippets • Zero external data exposure
        """)
        
        with gr.Tab("🔍 Search"):
            with gr.Row():
                with gr.Column(scale=3):
                    query_input = gr.Textbox(
                        label="Search Query",
                        placeholder="Ask a question or search for information...",
                        lines=2,
                        elem_classes=["search-box"]
                    )
                    
                    with gr.Row():
                        context_dropdown = gr.Dropdown(
                            choices=["auto", "hr", "technical", "safety", "general"],
                            value="auto",
                            label="Context (auto-detect by default)",
                            interactive=True
                        )
                        
                        top_k_slider = gr.Slider(
                            minimum=1,
                            maximum=20,
                            value=10,
                            step=1,
                            label="Number of Results"
                        )
                        
                        show_scores_checkbox = gr.Checkbox(
                            label="Show Scores",
                            value=True
                        )
                    
                    search_button = gr.Button("🔍 Search", variant="primary", size="lg")
                
                with gr.Column(scale=1):
                    context_info_output = gr.Markdown(label="Context Detection")
                    summary_output = gr.Markdown(label="Search Summary")
            
            results_output = gr.Markdown(label="Search Results", elem_classes=["results-container"])
            
            # Context-specific examples
            with gr.Accordion("💡 Example Queries", open=True):
                example_queries = get_example_queries()
                
                for context, queries in example_queries.items():
                    if context != "auto":
                        gr.Markdown(f"**{context.upper()}:**")
                        with gr.Row():
                            for query in queries[:3]:
                                gr.Button(query, size="sm").click(
                                    fn=lambda q=query, c=context: (q, c),
                                    outputs=[query_input, context_dropdown]
                                )
        
        with gr.Tab("📊 Analytics"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### System Statistics")
                    stats_button = gr.Button("📊 Get Statistics", variant="secondary")
                    stats_output = gr.Markdown()
                
                with gr.Column():
                    gr.Markdown("### System Diagnostics")
                    diagnostics_button = gr.Button("🔍 Run Diagnostics", variant="secondary")
                    diagnostics_output = gr.Markdown()
        
        with gr.Tab("❓ Help"):
            gr.Markdown("""
            ### How to Use OptimAIze Search
            
            **Basic Search:**
            - Type your question naturally: "How many vacation days do I get?"
            - The system will automatically detect the context
            - Results show the most relevant sections from your documents
            
            **Context Options:**
            - **Auto**: Let the system detect the context
            - **HR**: Employee policies, benefits, PTO
            - **Technical**: Engineering specs, design standards
            - **Safety**: Procedures, PPE, compliance
            - **General**: Any other queries
            
            **Search Tips:**
            - Use specific terms for better results
            - Questions work great: "What is..." "How do I..."
            - Try different phrasings if needed
            
            **Troubleshooting:**
            - No results? Run diagnostics to check system health
            - Poor results? Try specifying the context manually
            - Still issues? Check if documents are properly indexed
            """)
        
        # Event handlers
        search_button.click(
            fn=search_documents,
            inputs=[query_input, top_k_slider, context_dropdown, show_scores_checkbox],
            outputs=[results_output, summary_output, context_info_output]
        )
        
        query_input.submit(
            fn=search_documents,
            inputs=[query_input, top_k_slider, context_dropdown, show_scores_checkbox],
            outputs=[results_output, summary_output, context_info_output]
        )
        
        stats_button.click(
            fn=get_system_stats,
            outputs=stats_output
        )
        
        diagnostics_button.click(
            fn=run_diagnostics,
            outputs=diagnostics_output
        )
    
    return interface

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='OptimAIze Search UI')
    parser.add_argument('--api', action='store_true', help='Use API mode instead of direct search')
    parser.add_argument('--api-url', default='http://localhost:8000', help='API URL if using API mode')
    parser.add_argument('--share', action='store_true', help='Create public sharing link')
    args = parser.parse_args()
    
    if args.api:
        USE_API = True
        API_URL = args.api_url
        print(f"🌐 Using API mode: {API_URL}")
    else:
        print("🔍 Using direct search mode")
    
    print("🚀 Starting OptimAIze Search UI - Enterprise Edition...")
    print("🌐 Web interface will open automatically")
    print("📱 Access from other devices at: http://YOUR_IP:7860")
    print("\n✨ New Features:")
    print("  - Context-aware search")
    print("  - Interactive diagnostics")
    print("  - Query suggestions")
    print("  - Enhanced analytics")
    
    interface = create_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=args.share,
        debug=True
    )