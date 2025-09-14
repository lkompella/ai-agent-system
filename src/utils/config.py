"""
Configuration Management
"""

import os
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Config:
    """Application configuration"""
    
    # LLM Configuration
    llm_provider: str = "openai"
    llm_model: str = "gpt-4"
    openai_api_key: str = None
    anthropic_api_key: str = None
    max_response_tokens: int = 1000
    
    # RAG Configuration
    embedding_model: str = "all-MiniLM-L6-v2"
    vector_store_path: str = "./data/embeddings"
    chunk_size: int = 512
    chunk_overlap: int = 50
    
    # Database Configuration
    redis_url: str = "redis://localhost:6379"
    sqlite_db_path: str = "./data/agent.db"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False
    
    # Evaluation Configuration
    eval_enabled: bool = True
    eval_metrics: str = "relevance,accuracy,completeness"
    
    def __post_init__(self):
        """Load configuration from environment variables"""
        self._load_from_env()
        self._create_directories()
    
    def _load_from_env(self):
        """Load configuration from environment variables"""
        self.llm_provider = os.getenv("LLM_PROVIDER", self.llm_provider)
        self.llm_model = os.getenv("LLM_MODEL", self.llm_model)
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.max_response_tokens = int(os.getenv("MAX_RESPONSE_TOKENS", str(self.max_response_tokens)))
        
        self.embedding_model = os.getenv("EMBEDDING_MODEL", self.embedding_model)
        self.vector_store_path = os.getenv("VECTOR_STORE_PATH", self.vector_store_path)
        self.chunk_size = int(os.getenv("CHUNK_SIZE", str(self.chunk_size)))
        self.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", str(self.chunk_overlap)))
        
        self.redis_url = os.getenv("REDIS_URL", self.redis_url)
        self.sqlite_db_path = os.getenv("SQLITE_DB_PATH", self.sqlite_db_path)
        
        self.api_host = os.getenv("API_HOST", self.api_host)
        self.api_port = int(os.getenv("API_PORT", str(self.api_port)))
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        
        self.eval_enabled = os.getenv("EVAL_ENABLED", "true").lower() == "true"
        self.eval_metrics = os.getenv("EVAL_METRICS", self.eval_metrics)
    
    def _create_directories(self):
        """Create necessary directories"""
        directories = [
            Path(self.vector_store_path).parent,
            Path(self.sqlite_db_path).parent,
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
