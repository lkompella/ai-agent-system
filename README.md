# AI Agent with LLM + RAG + Eval + MCP + In-Memory Database

A comprehensive AI agent system that combines Large Language Models, Retrieval-Augmented Generation, Evaluation framework, Model Context Protocol, and in-memory database capabilities.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Client API    │◄──►│   Agent Core     │◄──►│   MCP Server    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────────────┐
        │                Agent Engine                      │
        │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐│
        │  │   LLM   │ │   RAG   │ │  Eval   │ │MemoryDB ││
        │  └─────────┘ └─────────┘ └─────────┘ └─────────┘│
        └─────────────────────────────────────────────────┘
```

## 📋 Prerequisites

- Python 3.9+
- Docker
- Redis (for caching)

## 🚀 Quick Start

1. **Setup Environment**:
   ```bash
   ./scripts/setup.sh
   cp .env.example .env
   # Edit .env with your API keys
   ```

2. **Run with Docker**:
   ```bash
   docker-compose up -d
   ```

3. **Test API**:
   ```bash
   curl http://localhost:8000/health
   ```

4. **Chat with Agent**:
   ```bash
   curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello! How can you help me?"}'
   ```

## 📖 Documentation

- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Interactive API**: http://localhost:8000/redoc

## 🔧 Components

- **LLM Integration**: OpenAI, Anthropic, Ollama support
- **RAG System**: Document retrieval with vector search
- **MCP Tools**: File search, calculator, text analysis
- **Evaluation**: Response quality metrics
- **Memory**: Redis + SQLite for persistence

## 🚀 Deployment

- **Local**: `docker-compose up -d`
- **AWS**: `./scripts/deploy.sh ecs`
- **Testing**: `./scripts/test.sh`

## 📁 Project Structure

```
ai-agent-system/
├── src/agent/          # Core agent logic
├── src/api/            # REST API
├── src/mcp/            # Tool integration
├── tests/              # Test suite
├── deployment/         # Docker & AWS configs
└── scripts/            # Setup & deployment
```

Happy building! 🎉
