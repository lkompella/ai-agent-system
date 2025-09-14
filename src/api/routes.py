"""
API Routes
Defines all API endpoints for the agent
"""

import logging
from typing import List
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends

from .models import ChatRequest, ChatResponse, HealthResponse
from ..agent.core import AIAgent

logger = logging.getLogger(__name__)

router = APIRouter()

def get_agent() -> AIAgent:
    """Dependency to get the global agent instance"""
    from .main import agent
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    return agent

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, agent: AIAgent = Depends(get_agent)):
    """Main chat endpoint"""
    try:
        response = await agent.process_query(
            query=request.message,
            session_id=request.session_id,
            use_rag=request.use_rag,
            use_tools=request.use_tools,
            evaluate=request.evaluate
        )
        
        return ChatResponse(
            message=response.message,
            confidence=response.confidence,
            sources=response.sources,
            tools_used=response.tools_used,
            evaluation_scores=response.evaluation_scores,
            session_id=response.session_id,
            metadata=response.metadata
        )
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents/upload")
async def upload_documents(
    files: List[UploadFile] = File(...),
    agent: AIAgent = Depends(get_agent)
):
    """Upload documents for RAG"""
    try:
        documents = []
        
        for file in files:
            content = await file.read()
            text_content = content.decode("utf-8", errors="ignore")
            
            documents.append({
                "content": text_content,
                "source": file.filename,
                "metadata": {
                    "content_type": file.content_type,
                    "size": len(content)
                }
            })
        
        success = await agent.add_documents(documents)
        
        return {
            "success": success,
            "document_count": len(documents),
            "message": f"Successfully uploaded {len(documents)} documents" if success else "Upload failed"
        }
        
    except Exception as e:
        logger.error(f"Document upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health", response_model=HealthResponse)
async def health_check(agent: AIAgent = Depends(get_agent)):
    """Overall health check"""
    try:
        health = await agent.health_check()
        return HealthResponse(**health)
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return HealthResponse(
            agent="unhealthy",
            timestamp="",
            components={},
            error=str(e)
        )

@router.get("/tools")
async def list_tools(agent: AIAgent = Depends(get_agent)):
    """List available MCP tools"""
    try:
        tools = await agent.get_available_tools()
        return {"tools": tools}
    except Exception as e:
        logger.error(f"Tool list error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
