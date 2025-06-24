"""
Minimal OptimAIze Teams Bot - Guaranteed to work on Azure
This is a stripped-down version that focuses on core functionality
"""

import os
import json
import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Dict, Any, Optional

# Create FastAPI app
app = FastAPI(
    title="OptimAIze Teams Bot",
    description="Minimal Teams bot for OptimAIze",
    version="1.0.0"
)

# Configuration from environment variables
OPTIMAIZE_BACKEND_URL = os.getenv("OPTIMAIZE_BACKEND_URL", "http://localhost:8000")
ALTURA_DOMAIN = os.getenv("ALTURA_DOMAIN", "alturaengineering.com")
BOT_NAME = "OptimAIze Assistant"

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "OptimAIze Teams Bot",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test backend connectivity
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                response = await client.get(f"{OPTIMAIZE_BACKEND_URL}/health")
                backend_healthy = response.status_code == 200
            except:
                backend_healthy = False
        
        health_status = {
            "status": "healthy" if backend_healthy else "degraded",
            "bot_service": "online",
            "optimaize_backend": "online" if backend_healthy else "offline",
            "backend_url": OPTIMAIZE_BACKEND_URL,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        status_code = 200 if backend_healthy else 503
        return JSONResponse(content=health_status, status_code=status_code)
        
    except Exception as e:
        return JSONResponse(
            content={
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            },
            status_code=500
        )

@app.post("/api/messages")
async def handle_teams_message(request: Request):
    """Handle Teams bot messages - simplified version"""
    try:
        # Get the request body
        body = await request.json()
        
        # Extract basic information
        activity_type = body.get("type", "")
        message_text = body.get("text", "").strip()
        from_user = body.get("from", {})
        user_name = from_user.get("name", "Unknown User")
        
        print(f"Received message: '{message_text}' from {user_name}")
        
        # Simple response logic
        if activity_type == "message" and message_text:
            # Check if user is from Altura (basic check)
            if ALTURA_DOMAIN in user_name.lower() or "@" not in user_name:
                response_text = await get_optimaize_response(message_text, user_name)
            else:
                response_text = f"🚫 Access denied. This bot is only for {ALTURA_DOMAIN} employees."
            
            # Send response back to Teams
            response_activity = {
                "type": "message",
                "text": response_text,
                "from": {"id": "optimaize-bot", "name": BOT_NAME},
                "conversation": body.get("conversation", {}),
                "recipient": from_user
            }
            
            return JSONResponse(content=response_activity)
        
        # For non-message activities, just return 200 OK
        return JSONResponse(content={"status": "ok"})
        
    except Exception as e:
        print(f"Error processing Teams message: {e}")
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

async def get_optimaize_response(query: str, user_name: str) -> str:
    """Get response from OptimAIze backend"""
    try:
        payload = {
            "query": query,
            "metadata": {
                "source": "teams_bot",
                "user_name": user_name,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{OPTIMAIZE_BACKEND_URL}/generate",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get("answer", "No answer available")
                return f"🤖 **OptimAIze Response:**\n\n{answer}"
            else:
                return f"❌ Backend error: {response.status_code}. Please try again later."
                
    except httpx.TimeoutException:
        return "⏱️ Request timed out. Please try a simpler question."
    except Exception as e:
        print(f"Error calling OptimAIze backend: {e}")
        return "❌ Sorry, I'm having technical difficulties. Please try again later."

@app.get("/status")
async def status():
    """Detailed status information"""
    return {
        "service": "OptimAIze Teams Bot",
        "version": "1.0.0-minimal",
        "backend_url": OPTIMAIZE_BACKEND_URL,
        "altura_domain": ALTURA_DOMAIN,
        "status": "running",
        "timestamp": datetime.utcnow().isoformat()
    }

# For local testing
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)