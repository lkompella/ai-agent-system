#!/bin/bash

# Simple API test script

echo "🧪 Testing AI Agent API..."

BASE_URL="http://localhost:8000"

# Test health endpoint
echo "1. Testing health endpoint..."
curl -f "$BASE_URL/health" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed"
    exit 1
fi

# Test chat endpoint
echo "2. Testing chat endpoint..."
response=$(curl -s -X POST "$BASE_URL/chat" \
    -H "Content-Type: application/json" \
    -d '{"message": "Hello, how are you?"}')

if echo "$response" | grep -q "message"; then
    echo "✅ Chat endpoint test passed"
    echo "Response: $(echo "$response" | head -c 100)..."
else
    echo "❌ Chat endpoint test failed"
    echo "Response: $response"
fi

echo "🎉 API tests completed!"
