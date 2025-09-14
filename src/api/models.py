"""
Pydantic Models for API
Request and response models for all endpoints
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    """Chat request model"""
    message: str = Field(..., description="User message")
    session_id: Optional[str] = Field(None, description="Session ID for conversation context")
    use_rag: bool = Field(True, description="Enable RAG for response generation")
    use_tools: bool = Field(True, description="Enable tool usage")
    evaluate: bool = Field(True, description="Enable response evaluation")
    max_tokens: Optional[int] = Field(None, description="Maximum tokens for response")

class ChatResponse(BaseModel):
    """Chat response model"""
    message: str = Field(..., description="Agent response")
    confidence: float = Field(..., description="Response confidence score")
    sources: List[str] = Field(default_factory=list, description="Sources used for RAG")
    tools_used: List[str] = Field(default_factory=list, description="Tools used in response")
    evaluation_scores: Dict[str, float] = Field(default_factory=dict, description="Evaluation metric scores")
    session_id: str = Field(..., description="Session ID")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

class HealthResponse(BaseModel):
    """Health check response model"""
    agent: str = Field(..., description="Overall agent status")
    timestamp: str = Field(..., description="Health check timestamp")
    components: Dict[str, Any] = Field(default_factory=dict, description="Component health status")
    error: Optional[str] = Field(None, description="Error message if unhealthy")
