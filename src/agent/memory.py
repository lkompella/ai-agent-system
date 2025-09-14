"""
In-Memory Database Implementation (Simplified)
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class MemoryDatabase:
    """Simplified memory database for demo"""
    
    def __init__(self, config):
        self.config = config
        self.conversations = {}  # In-memory storage for demo
    
    async def initialize(self):
        """Initialize the memory database"""
        logger.info("Memory database initialized")
    
    async def store_interaction(
        self,
        session_id: str,
        query: str,
        response: str,
        sources: List[str],
        tools_used: List[str],
        evaluation_scores: Dict[str, float],
        metadata: Dict[str, Any] = None
    ):
        """Store a complete interaction"""
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        
        interaction = {
            "query": query,
            "response": response,
            "sources": sources,
            "tools_used": tools_used,
            "evaluation_scores": evaluation_scores,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.conversations[session_id].append(interaction)
        
        # Keep only last 50 interactions per session
        if len(self.conversations[session_id]) > 50:
            self.conversations[session_id] = self.conversations[session_id][-50:]
    
    async def get_conversation_history(self, session_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get conversation history for a session"""
        if session_id not in self.conversations:
            return []
        
        return self.conversations[session_id][-limit:]
    
    async def clear_conversation_history(self, session_id: str) -> bool:
        """Clear conversation history for a session"""
        if session_id in self.conversations:
            del self.conversations[session_id]
            return True
        return False
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check for memory database"""
        return {
            "status": "healthy",
            "active_sessions": len(self.conversations)
        }
