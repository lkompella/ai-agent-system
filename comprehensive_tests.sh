# simple_tests.sh - Quick and easy tests for AI Agent

#!/bin/bash

BASE_URL="http://localhost:8000"
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 Quick AI Agent Tests${NC}"
echo "======================="

echo -e "${BLUE}1. Health Check${NC}"
curl -s "$BASE_URL/health" | jq '.'
echo ""

echo -e "${BLUE}2. Simple Chat${NC}"
curl -s -X POST "$BASE_URL/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello! Tell me what you can do."}' | jq '.'
echo ""

echo -e "${BLUE}3. Calculator Test${NC}"
curl -s -X POST "$BASE_URL/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Calculate 15 * 8 + 32"}' | jq '.'
echo ""

echo -e "${BLUE}4. File Search Test${NC}"
curl -s -X POST "$BASE_URL/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Find Python files in the src directory"}' | jq '.'
echo ""

echo -e "${BLUE}5. Available Tools${NC}"
curl -s "$BASE_URL/tools" | jq '.'
echo ""

echo -e "${GREEN}✅ Quick tests completed!${NC}"

# Individual test functions you can call
test_basic_chat() {
    echo "Testing basic chat..."
    curl -s -X POST "$BASE_URL/chat" \
        -H "Content-Type: application/json" \
        -d '{"message": "'"$1"'"}' | jq '.message'
}

test_with_session() {
    echo "Testing with session..."
    curl -s -X POST "$BASE_URL/chat" \
        -H "Content-Type: application/json" \
        -d '{"message": "'"$1"'", "session_id": "'"$2"'"}' | jq '.message'
}

upload_test_doc() {
    echo "Test document content about AI and machine learning." > /tmp/test.txt
    curl -s -X POST "$BASE_URL/documents/upload" \
        -F "files=@/tmp/test.txt" | jq '.'
    rm /tmp/test.txt
}

# Examples of how to use these functions:
# test_basic_chat "What is artificial intelligence?"
# test_with_session "My name is John" "test-session-1" 
# test_with_session "What's my name?" "test-session-1"
# upload_test_doc