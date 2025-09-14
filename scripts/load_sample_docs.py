#!/usr/bin/env python3
"""
Load sample documents for testing
"""

import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agent.core import AIAgent
from utils.config import Config

async def load_sample_documents():
    """Load sample documents for testing"""
    
    sample_docs = [
        {
            "content": "Machine learning is a subset of AI that enables systems to learn from data.",
            "source": "ml_basics.txt",
            "metadata": {"topic": "machine_learning"}
        },
        {
            "content": "Python is a versatile programming language used for web development, data science, and AI.",
            "source": "python_intro.txt",
            "metadata": {"topic": "programming"}
        },
        {
            "content": "FastAPI is a modern Python web framework for building APIs quickly and efficiently.",
            "source": "fastapi_guide.txt", 
            "metadata": {"topic": "web_development"}
        }
    ]
    
    print("📚 Loading sample documents...")
    config = Config()
    agent = AIAgent(config)
    await agent.initialize()
    
    success = await agent.add_documents(sample_docs)
    
    if success:
        print("✅ Sample documents loaded successfully!")
    else:
        print("❌ Failed to load sample documents")

if __name__ == "__main__":
    asyncio.run(load_sample_documents())
