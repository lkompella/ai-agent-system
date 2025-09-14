"""
Core Agent Implementation
Orchestrates LLM, RAG, MCP, and Evaluation components
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

from .llm import LLMManager
from .rag import RAGSystem
from .memory import MemoryDatabase
from .evaluator import EvaluationFramework
from ..mcp.client import MCPClient
from ..utils.config import Config

logger = logging.getLogger(__name__)

@dataclass
class AgentResponse:
    """Agent response structure"""
    message: str
    confidence: float
    sources: List[str]
    tools_used: List[str]
    evaluation_scores: Dict[str, float]
    session_id: str
    timestamp: datetime
    metadata: Dict[str, Any]

class AIAgent:
    """Main AI Agent class that integrates all components"""
    
    def __init__(self, config: Config):
        self.config = config
        self.session_id = None
        
        # Initialize components
        self.llm_manager = LLMManager(config)
        self.rag_system = RAGSystem(config)
        self.memory_db = MemoryDatabase(config)
        self.evaluator = EvaluationFramework(config)
        self.mcp_client = MCPClient(config)
        
        logger.info("AI Agent initialized successfully")
    
    async def initialize(self):
        """Initialize all async components"""
        await self.memory_db.initialize()
        await self.rag_system.initialize()
        await self.mcp_client.initialize()
        logger.info("AI Agent async initialization completed")
    
    async def process_query(
        self,
        query: str,
        session_id: Optional[str] = None,
        use_rag: bool = True,
        use_tools: bool = True,
        evaluate: bool = True
    ) -> AgentResponse:
        """Process a user query through the complete agent pipeline"""
        start_time = datetime.now()
        session_id = session_id or self._generate_session_id()
        
        try:
            # Step 1: Retrieve conversation history
            conversation_history = await self.memory_db.get_conversation_history(session_id)
            
            # Step 2: RAG retrieval (if enabled)
            rag_context = ""
            sources = []
            if use_rag:
                rag_results = await self.rag_system.retrieve(query)
                rag_context = "\n".join([doc.content for doc in rag_results])
                sources = [doc.source for doc in rag_results]
            
            # Step 3: Tool execution (if enabled)
            tools_used = []
            tool_results = ""
            if use_tools:
                tool_calls = await self._identify_tool_calls(query)
                for tool_call in tool_calls:
                    result = await self.mcp_client.execute_tool(
                        tool_call["name"], 
                        tool_call["parameters"]
                    )
                    tools_used.append(tool_call["name"])
                    tool_results += f"\nTool {tool_call['name']}: {result}"
            
            # Step 4: Generate LLM response
            context = self._build_context(
                query=query,
                conversation_history=conversation_history,
                rag_context=rag_context,
                tool_results=tool_results
            )
            
            llm_response = await self.llm_manager.generate_response(
                context=context,
                max_tokens=self.config.max_response_tokens
            )
            
            # Step 5: Evaluate response (if enabled)
            evaluation_scores = {}
            if evaluate:
                evaluation_scores = await self.evaluator.evaluate_response(
                    query=query,
                    response=llm_response,
                    context=rag_context,
                    sources=sources,
                    start_time=start_time
                )
            
            # Step 6: Store in memory
            await self.memory_db.store_interaction(
                session_id=session_id,
                query=query,
                response=llm_response,
                sources=sources,
                tools_used=tools_used,
                evaluation_scores=evaluation_scores
            )
            
            # Step 7: Calculate confidence score
            confidence = self._calculate_confidence(evaluation_scores, sources, tools_used)
            
            # Build response
            response = AgentResponse(
                message=llm_response,
                confidence=confidence,
                sources=sources,
                tools_used=tools_used,
                evaluation_scores=evaluation_scores,
                session_id=session_id,
                timestamp=start_time,
                metadata={
                    "processing_time": (datetime.now() - start_time).total_seconds(),
                    "rag_enabled": use_rag,
                    "tools_enabled": use_tools,
                    "evaluation_enabled": evaluate
                }
            )
            
            logger.info(f"Query processed successfully for session {session_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            raise
    
    async def add_documents(self, documents: List[Dict[str, Any]]) -> bool:
        """Add documents to the RAG system"""
        try:
            return await self.rag_system.add_documents(documents)
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            return False
    
    async def get_conversation_history(self, session_id: str) -> List[Dict]:
        """Retrieve conversation history for a session"""
        return await self.memory_db.get_conversation_history(session_id)
    
    async def clear_conversation_history(self, session_id: str) -> bool:
        """Clear conversation history for a session"""
        return await self.memory_db.clear_conversation_history(session_id)
    
    async def get_available_tools(self) -> List[Dict]:
        """Get list of available MCP tools"""
        return await self.mcp_client.get_available_tools()
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on all components"""
        health_status = {
            "agent": "healthy",
            "timestamp": datetime.now().isoformat(),
            "components": {}
        }
        
        try:
            # Check components
            health_status["components"]["llm"] = await self.llm_manager.health_check()
            health_status["components"]["rag"] = await self.rag_system.health_check()
            health_status["components"]["memory"] = await self.memory_db.health_check()
            health_status["components"]["mcp"] = await self.mcp_client.health_check()
            health_status["components"]["evaluator"] = self.evaluator.health_check()
            
        except Exception as e:
            health_status["agent"] = "unhealthy"
            health_status["error"] = str(e)
        
        return health_status
    
    def _build_context(self, query: str, conversation_history: List[Dict], 
                      rag_context: str, tool_results: str) -> str:
        """Build context for LLM generation"""
        context_parts = []
        
        if conversation_history:
            history_text = "\n".join([
                f"User: {item['query']}\nAssistant: {item['response']}"
                for item in conversation_history[-5:]  # Last 5 interactions
            ])
            context_parts.append(f"Conversation History:\n{history_text}")
        
        if rag_context:
            context_parts.append(f"Relevant Information:\n{rag_context}")
        
        if tool_results:
            context_parts.append(f"Tool Results:\n{tool_results}")
        
        context_parts.append(f"Current Query: {query}")
        
        return "\n\n".join(context_parts)
    
    async def _identify_tool_calls(self, query: str) -> List[Dict]:
        """Identify which tools should be called based on the query"""
        tool_calls = []
        
        if "search" in query.lower() or "find" in query.lower():
            tool_calls.append({
                "name": "file_search",
                "parameters": {"pattern": "*.py", "directory": "./src"}
            })
        
        if "calculate" in query.lower() or "compute" in query.lower():
            tool_calls.append({
                "name": "calculator",
                "parameters": {"expression": query}
            })
        
        return tool_calls
    
    def _calculate_confidence(self, evaluation_scores: Dict[str, float], 
                            sources: List[str], tools_used: List[str]) -> float:
        """Calculate confidence score based on various factors"""
        base_confidence = 0.5
        
        if evaluation_scores:
            avg_eval_score = sum(evaluation_scores.values()) / len(evaluation_scores)
            base_confidence += 0.3 * avg_eval_score
        
        if sources:
            base_confidence += min(0.2, len(sources) * 0.05)
        
        if tools_used:
            base_confidence += min(0.1, len(tools_used) * 0.05)
        
        return min(1.0, base_confidence)
    
    def _generate_session_id(self) -> str:
        """Generate a unique session ID"""
        import uuid
        return str(uuid.uuid4())
