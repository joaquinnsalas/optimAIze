import httpx
import structlog
from typing import Dict, Any, Optional
from datetime import datetime
from config import config

logger = structlog.get_logger(__name__)

class OptimAIzeClient:
    """HTTP client for communicating with the OptimAIze FastAPI backend"""
    
    def __init__(self):
        self.base_url = config.optimaize_backend_url.rstrip('/')
        self.timeout = config.optimaize_api_timeout
        self.session = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = httpx.AsyncClient(
            timeout=httpx.Timeout(self.timeout),
            headers={
                "Content-Type": "application/json",
                "User-Agent": "OptimAIze-Teams-Bot/1.0"
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.aclose()
    
    async def health_check(self) -> bool:
        """Check if the OptimAIze backend is healthy"""
        try:
            response = await self.session.get(f"{self.base_url}/health")
            return response.status_code == 200
        except Exception as e:
            logger.error("Health check failed", error=str(e))
            return False
    
    async def generate_response(
        self, 
        query: str, 
        user_id: str, 
        user_email: str,
        conversation_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send a query to the OptimAIze /generate endpoint
        
        Args:
            query: User's question
            user_id: Teams user ID
            user_email: User's email address
            conversation_id: Teams conversation ID
            context: Additional context from Teams
            
        Returns:
            Dict containing the response from OptimAIze backend
        """
        try:
            # Prepare the request payload
            payload = {
                "query": query,
                "metadata": {
                    "source": "teams_bot",
                    "user_id": user_id,
                    "user_email": user_email,
                    "timestamp": datetime.utcnow().isoformat(),
                    "conversation_id": conversation_id,
                    "context": context or {}
                }
            }
            
            logger.info(
                "Sending query to OptimAIze backend",
                user_email=user_email,
                query_length=len(query),
                conversation_id=conversation_id
            )
            
            # Make the API call
            response = await self.session.post(
                f"{self.base_url}/generate",
                json=payload
            )
            
            response.raise_for_status()
            result = response.json()
            
            logger.info(
                "Received response from OptimAIze backend",
                user_email=user_email,
                response_length=len(result.get("answer", "")),
                status_code=response.status_code
            )
            
            return result
            
        except httpx.HTTPStatusError as e:
            logger.error(
                "HTTP error from OptimAIze backend",
                status_code=e.response.status_code,
                error_detail=e.response.text,
                user_email=user_email
            )
            return {
                "error": f"Backend service error: {e.response.status_code}",
                "answer": "Sorry, I'm experiencing technical difficulties. Please try again later."
            }
            
        except httpx.TimeoutException:
            logger.error(
                "Timeout calling OptimAIze backend",
                user_email=user_email,
                timeout=self.timeout
            )
            return {
                "error": "Request timeout",
                "answer": "The request is taking longer than expected. Please try again with a simpler question."
            }
            
        except Exception as e:
            logger.error(
                "Unexpected error calling OptimAIze backend",
                error=str(e),
                user_email=user_email
            )
            return {
                "error": f"Unexpected error: {str(e)}",
                "answer": "Sorry, something went wrong. Please try again later."
            }
    
    async def search_documents(
        self, 
        query: str, 
        user_id: str, 
        user_email: str,
        limit: int = 5
    ) -> Dict[str, Any]:
        """
        Search documents using the OptimAIze /search endpoint
        
        Args:
            query: Search query
            user_id: Teams user ID
            user_email: User's email address
            limit: Number of results to return
            
        Returns:
            Dict containing search results
        """
        try:
            payload = {
                "query": query,
                "limit": limit,
                "metadata": {
                    "source": "teams_bot",
                    "user_id": user_id,
                    "user_email": user_email,
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
            
            response = await self.session.post(
                f"{self.base_url}/search",
                json=payload
            )
            
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(
                "Error searching documents",
                error=str(e),
                user_email=user_email
            )
            return {
                "error": str(e),
                "results": []
            }

# Utility function for easy client usage
async def get_optimaize_response(
    query: str, 
    user_id: str, 
    user_email: str,
    conversation_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Convenience function to get a response from OptimAIze
    """
    async with OptimAIzeClient() as client:
        return await client.generate_response(
            query=query,
            user_id=user_id,
            user_email=user_email,
            conversation_id=conversation_id,
            context=context
        )