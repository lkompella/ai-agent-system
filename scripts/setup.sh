#!/bin/bash

echo "🚀 Setting up AI Agent System..."

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oP '(?<=Python )\d+\.\d+')
if [[ $(echo "$python_version < 3.9" | bc -l 2>/dev/null || echo 1) -eq 1 ]]; then
    echo "❌ Python 3.9+ is required. Current version: $python_version"
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data/{documents,embeddings,evaluations}
mkdir -p logs

# Create sample .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️ Please edit .env file with your API keys and configuration"
fi

echo "✅ Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Edit the .env file with your API keys"
echo "2. Run 'source venv/bin/activate' to activate the virtual environment"
echo "3. Run 'python -m uvicorn src.api.main:app --reload' to start the server"
echo "4. Visit http://localhost:8000/docs to see the API documentation"
