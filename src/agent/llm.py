"""
LLM Manager Implementation
Handles multiple LLM providers and model selection
"""

import asyncio
import logging
from typing import Dict, Optional, Any
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class BaseLLM(ABC):
    """Base class for LLM implementations"""
    
    @abstractmethod
    async def generate_response(self, context: str, max_tokens: int = 1000) -> str:
        pass
    
    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        pass

class MockLLM(BaseLLM):
    """Mock LLM for testing and demo purposes"""
    
    def __init__(self, model: str = "mock-model"):
        self.model = model
    
    async def generate_response(self, context: str, max_tokens: int = 1000) -> str:
        """Generate a mock response"""
        await asyncio.sleep(0.1)  # Simulate API delay
        
        # Simple response based on context
        if "hello" in context.lower():
            return "Hello! I'm an AI agent ready to help you with various tasks. I can process documents, use tools, and provide evaluated responses."
        elif "machine learning" in context.lower():
            return "Machine learning is a subset of AI that enables systems to learn and improve from data without explicit programming. It includes supervised, unsupervised, and reinforcement learning approaches."
        elif "calculate" in context.lower() or "compute" in context.lower():
            return "I can help with calculations using my built-in calculator tool. What would you like me to compute?"
        else:
            return f"I understand you're asking about: {context[:100]}... Let me help you with that. This is a comprehensive AI agent that can process your requests using RAG, tools, and evaluation systems."
    
    async def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy", "model": self.model, "type": "mock"}

class OpenAILLM(BaseLLM):
    """OpenAI LLM implementation"""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        
        # Only import and initialize if we have a real API key
        if api_key and api_key != "your_openai_api_key_here" and api_key != "test-key":
            try:
                import openai
                self.client = openai.AsyncOpenAI(api_key=api_key)
                self.enabled = True
            except ImportError:
                logger.warning("OpenAI package not available, using mock LLM")
                self.enabled = False
        else:
            self.enabled = False
            logger.info("No valid OpenAI API key, using mock LLM")
    
    async def generate_response(self, context: str, max_tokens: int = 1000) -> str:
        if not self.enabled:
            # Fall back to mock behavior
            mock_llm = MockLLM(self.model)
            return await mock_llm.generate_response(context, max_tokens)
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": context}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            # Fall back to mock
            mock_llm = MockLLM(self.model)
            return await mock_llm.generate_response(context, max_tokens)
    
    async def health_check(self) -> Dict[str, Any]:
        if not self.enabled:
            return {"status": "mock", "model": self.model, "reason": "No API key"}
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            return {"status": "healthy", "model": self.model}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e), "model": self.model}

class LLMManager:
    """Manager for handling multiple LLM providers"""
    
    def __init__(self, config):
        self.config = config
        self.llm = self._initialize_llm()
    
    def _initialize_llm(self) -> BaseLLM:
        """Initialize the appropriate LLM based on configuration"""
        provider = self.config.llm_provider.lower()
        
        if provider == "openai":
            return OpenAILLM(
                api_key=self.config.openai_api_key,
                model=self.config.llm_model
            )
        else:
            # Default to mock for demo purposes
            return MockLLM(self.config.llm_model)
    
    async def generate_response(self, context: str, max_tokens: int = 1000) -> str:
        """Generate response using the configured LLM"""
        return await self.llm.generate_response(context, max_tokens)
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on the LLM"""
        return await self.llm.health_check()
