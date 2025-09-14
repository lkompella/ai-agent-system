"""
FastAPI Application
Main API server for the AI Agent
"""

import logging
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router
from ..agent.core import AIAgent
from ..utils.config import Config
from ..utils.logging import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Global agent instance
agent: Optional[AIAgent] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global agent
    
    # Startup
    logger.info("Starting AI Agent API server...")
    
    # Load configuration
    config = Config()
    
    # Initialize agent
    agent = AIAgent(config)
    await agent.initialize()
    
    logger.info("AI Agent API server started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI Agent API server...")

# Create FastAPI app
app = FastAPI(
    title="AI Agent API",
    description="Comprehensive AI Agent with LLM + RAG + Eval + MCP + In-Memory Database",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "AI Agent API is running", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
