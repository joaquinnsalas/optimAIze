"""Ollama HTTP client for LLM inference."""

import asyncio
import aiohttp
import json
import time
from typing import Dict, Any, Optional, Tuple
from src.utils.logger import logger
from src.llm.models import OllamaRequest, OllamaResponse, LLMError

class OllamaClient:
    """HTTP client for Ollama API communication."""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url.rstrip('/')
        self.generate_url = f"{self.base_url}/api/generate"
        self.models_url = f"{self.base_url}/api/tags"
        self.session = None
        
        # Default timeouts
        self.connect_timeout = 10.0
        self.read_timeout = 120.0  # LLM generation can be slow
        
        logger.info(f"Ollama client initialized for {self.base_url}")
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(
                connect=self.connect_timeout,
                total=self.read_timeout
            )
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    async def health_check(self) -> Tuple[bool, Optional[str]]:
        """Check if Ollama is available and responsive."""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession(
                    timeout=aiohttp.ClientTimeout(connect=5.0, total=10.0)
                )
            
            async with self.session.get(self.models_url) as response:
                if response.status == 200:
                    data = await response.json()
                    models = [model.get("name", "unknown") for model in data.get("models", [])]
                    logger.debug(f"Ollama available with models: {models}")
                    return True, f"Available models: {', '.join(models)}"
                else:
                    error_msg = f"Ollama responded with status {response.status}"
                    logger.warning(error_msg)
                    return False, error_msg
        
        except asyncio.TimeoutError:
            error_msg = "Ollama health check timed out"
            logger.warning(error_msg)
            return False, error_msg
        except aiohttp.ClientConnectorError:
            error_msg = "Could not connect to Ollama (connection refused)"
            logger.warning(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Ollama health check failed: {e}"
            logger.error(error_msg)
            return False, error_msg
    
    async def generate(self, request: OllamaRequest) -> Tuple[Optional[OllamaResponse], Optional[LLMError]]:
        """Generate text using Ollama."""
        start_time = time.time()
        
        try:
            # Ensure we have a session
            if not self.session:
                self.session = aiohttp.ClientSession(
                    timeout=aiohttp.ClientTimeout(
                        connect=self.connect_timeout,
                        total=self.read_timeout
                    )
                )
            
            # Prepare request data
            request_data = {
                "model": request.model,
                "prompt": request.prompt,
                "stream": request.stream,
                "options": request.options
            }
            
            logger.info(f"Generating with model '{request.model}' (prompt length: {len(request.prompt)} chars)")
            
            # Make the request
            async with self.session.post(
                self.generate_url,
                json=request_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status != 200:
                    error_text = await response.text()
                    error_msg = f"Ollama generation failed with status {response.status}: {error_text}"
                    logger.error(error_msg)
                    
                    return None, LLMError(
                        error_type="api_error",
                        error_message=error_msg
                    )
                
                # Parse response
                response_text = await response.text()
                
                # Handle streaming vs non-streaming responses
                if request.stream:
                    # For streaming, we need to parse the last complete JSON object
                    lines = response_text.strip().split('\n')
                    last_response = None
                    
                    for line in lines:
                        try:
                            data = json.loads(line)
                            if data.get("done", False):
                                last_response = data
                                break
                        except json.JSONDecodeError:
                            continue
                    
                    if not last_response:
                        error_msg = "Could not parse streaming response"
                        logger.error(error_msg)
                        return None, LLMError(
                            error_type="parse_error",
                            error_message=error_msg
                        )
                    
                    response_data = last_response
                else:
                    # Non-streaming response
                    try:
                        response_data = json.loads(response_text)
                    except json.JSONDecodeError as e:
                        error_msg = f"Could not parse Ollama response: {e}"
                        logger.error(error_msg)
                        return None, LLMError(
                            error_type="parse_error",
                            error_message=error_msg
                        )
                
                # Create response object
                ollama_response = OllamaResponse(
                    model=response_data.get("model", request.model),
                    response=response_data.get("response", ""),
                    done=response_data.get("done", True),
                    total_duration=response_data.get("total_duration"),
                    load_duration=response_data.get("load_duration"),
                    prompt_eval_count=response_data.get("prompt_eval_count"),
                    prompt_eval_duration=response_data.get("prompt_eval_duration"),
                    eval_count=response_data.get("eval_count"),
                    eval_duration=response_data.get("eval_duration")
                )
                
                generation_time = (time.time() - start_time) * 1000
                logger.info(f"Generation completed in {generation_time:.1f}ms")
                logger.debug(f"Generated {len(ollama_response.response)} characters")
                
                return ollama_response, None
        
        except asyncio.TimeoutError:
            error_msg = f"Ollama generation timed out after {self.read_timeout}s"
            logger.error(error_msg)
            return None, LLMError(
                error_type="timeout",
                error_message=error_msg
            )
        
        except aiohttp.ClientConnectorError:
            error_msg = "Could not connect to Ollama (connection refused)"
            logger.error(error_msg)
            return None, LLMError(
                error_type="connection_error",
                error_message=error_msg
            )
        
        except Exception as e:
            error_msg = f"Unexpected error during generation: {e}"
            logger.error(error_msg)
            return None, LLMError(
                error_type="unexpected_error",
                error_message=error_msg
            )
    
    async def list_models(self) -> Tuple[Optional[list], Optional[str]]:
        """List available models in Ollama."""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession(
                    timeout=aiohttp.ClientTimeout(connect=5.0, total=10.0)
                )
            
            async with self.session.get(self.models_url) as response:
                if response.status == 200:
                    data = await response.json()
                    models = [model.get("name", "unknown") for model in data.get("models", [])]
                    return models, None
                else:
                    error_msg = f"Failed to list models: status {response.status}"
                    return None, error_msg
        
        except Exception as e:
            error_msg = f"Error listing models: {e}"
            logger.error(error_msg)
            return None, error_msg

# Global instance
ollama_client = OllamaClient()