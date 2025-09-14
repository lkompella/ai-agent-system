"""
Basic tests for the AI Agent
"""

import pytest
import asyncio
from unittest.mock import Mock

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agent.core import AIAgent
from utils.config import Config

@pytest.fixture
def mock_config():
    """Mock configuration for testing"""
    config = Mock(spec=Config)
    config.llm_provider = "openai"
    config.llm_model = "gpt-4"
    config.openai_api_key = "test-key"
    config.max_response_tokens = 1000
    return config

@pytest.mark.asyncio
async def test_agent_initialization(mock_config):
    """Test agent initialization"""
    agent = AIAgent(mock_config)
    assert agent is not None
    assert agent.config == mock_config

@pytest.mark.asyncio
async def test_health_check():
    """Test basic health check"""
    config = Config()
    agent = AIAgent(config)
    await agent.initialize()
    
    health = await agent.health_check()
    assert "agent" in health
    assert "components" in health
