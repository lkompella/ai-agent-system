# interactive_test.py - Interactive testing for AI Agent

import requests
import json
import time
import sys
from pathlib import Path

class AIAgentTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_session_id = f"test-session-{int(time.time())}"
    
    def print_response(self, response, title="Response"):
        """Pretty print API response"""
        print(f"\n🔍 {title}:")
        print("=" * 50)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            
            # Pretty print key fields
            if 'message' in data:
                print(f"💬 Message: {data['message'][:200]}...")
            if 'confidence' in data:
                print(f"📊 Confidence: {data['confidence']:.2f}")
            if 'sources' in data and data['sources']:
                print(f"📚 Sources: {', '.join(data['sources'])}")
            if 'tools_used' in data and data['tools_used']:
                print(f"🔧 Tools Used: {', '.join(data['tools_used'])}")
            if 'evaluation_scores' in data and data['evaluation_scores']:
                print(f"📈 Evaluation Scores:")
                for metric, score in data['evaluation_scores'].items():
                    print(f"  {metric}: {score:.2f}")
                    
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"Error: {response.text}")
    
    def test_basic_chat(self):
        """Test basic chat functionality"""
        print("\n🚀 Testing Basic Chat...")
        
        test_messages = [
            "Hello! Can you introduce yourself?",
            "What can you help me with?",
            "Tell me about your capabilities",
        ]
        
        for msg in test_messages:
            print(f"\n📤 Sending: {msg}")
            response = self.session.post(
                f"{self.base_url}/chat",
                json={
                    "message": msg,
                    "session_id": self.test_session_id
                }
            )
            self.print_response(response, f"Chat Response")
            time.sleep(1)  # Small delay between requests
    
    def test_rag_system(self):
        """Test RAG system with document upload"""
        print("\n📚 Testing RAG System...")
        
        # Create a test document
        test_content = """
        Artificial Intelligence (AI) is transforming industries worldwide. 
        Key areas include:
        1. Machine Learning - algorithms that learn from data
        2. Natural Language Processing - understanding human language
        3. Computer Vision - interpreting visual information
        4. Robotics - AI-powered automation
        
        Popular frameworks include TensorFlow, PyTorch, and scikit-learn.
        Applications span healthcare, finance, transportation, and entertainment.
        """
        
        # Save to temporary file
        test_file_path = Path("/tmp/ai_overview.txt")
        test_file_path.write_text(test_content)
        
        # Upload document
        print("📤 Uploading test document...")
        with open(test_file_path, 'rb') as f:
            files = {'files': ('ai_overview.txt', f, 'text/plain')}
            response = self.session.post(f"{self.base_url}/documents/upload", files=files)
        
        self.print_response(response, "Document Upload")
        
        # Test RAG queries
        rag_questions = [
            "What AI frameworks are mentioned in my document?",
            "Which industries are being transformed by AI?",
            "Tell me about the key areas of AI from the document",
        ]
        
        for question in rag_questions:
            print(f"\n📤 RAG Query: {question}")
            response = self.session.post(
                f"{self.base_url}/chat",
                json={
                    "message": question,
                    "session_id": self.test_session_id,
                    "use_rag": True
                }
            )
            self.print_response(response, "RAG Response")
            time.sleep(1)
        
        # Clean up
        test_file_path.unlink(missing_ok=True)
    
    def test_mcp_tools(self):
        """Test MCP tools functionality"""
        print("\n🔧 Testing MCP Tools...")
        
        # First, list available tools
        print("📤 Getting available tools...")
        response = self.session.get(f"{self.base_url}/tools")
        self.print_response(response, "Available Tools")
        
        # Test calculator tool
        calc_questions = [
            "Calculate 25 * 4 + 17",
            "What is 100 / 8?",
            "Compute (15 + 25) * 2",
        ]
        
        for calc in calc_questions:
            print(f"\n📤 Calculator: {calc}")
            response = self.session.post(
                f"{self.base_url}/chat",
                json={
                    "message": calc,
                    "session_id": self.test_session_id,
                    "use_tools": True
                }
            )
            self.print_response(response, "Calculator Response")
            time.sleep(1)
        
        # Test file search tool
        search_questions = [
            "Find Python files in the src directory",
            "Search for configuration files",
            "Look for test files",
        ]
        
        for search in search_questions:
            print(f"\n📤 File Search: {search}")
            response = self.session.post(
                f"{self.base_url}/chat",
                json={
                    "message": search,
                    "session_id": self.test_session_id,
                    "use_tools": True
                }
            )
            self.print_response(response, "File Search Response")
            time.sleep(1)
    
    def test_evaluation_system(self):
        """Test evaluation system"""
        print("\n📈 Testing Evaluation System...")
        
        test_scenarios = [
            {
                "message": "What is the capital of France?",
                "description": "Simple factual query"
            },
            {
                "message": "Explain quantum computing in detail with examples and applications",
                "description": "Complex explanatory query"
            },
            {
                "message": "Hello",
                "description": "Simple greeting"
            }
        ]
        
        for scenario in test_scenarios:
            print(f"\n📤 {scenario['description']}: {scenario['message']}")
            response = self.session.post(
                f"{self.base_url}/chat",
                json={
                    "message": scenario['message'],
                    "session_id": self.test_session_id,
                    "evaluate": True
                }
            )
            self.print_response(response, f"Evaluation Test - {scenario['description']}")
            time.sleep(1)
    
    def test_conversation_context(self):
        """Test conversation context and memory"""
        print("\n💭 Testing Conversation Context...")
        
        conversation_flow = [
            "My favorite programming language is Python.",
            "I also like machine learning.",
            "What programming language did I mention?",
            "What topics am I interested in?",
            "Can you summarize our conversation so far?"
        ]
        
        context_session = f"context-test-{int(time.time())}"
        
        for i, message in enumerate(conversation_flow, 1):
            print(f"\n📤 Step {i}: {message}")
            response = self.session.post(
                f"{self.base_url}/chat",
                json={
                    "message": message,
                    "session_id": context_session
                }
            )
            self.print_response(response, f"Context Step {i}")
            time.sleep(1)
    
    def test_health_monitoring(self):
        """Test health monitoring endpoints"""
        print("\n❤️ Testing Health Monitoring...")
        
        health_endpoints = [
            "/health",
            "/health/llm", 
            "/health/rag",
            "/health/mcp",
            "/health/database"
        ]
        
        for endpoint in health_endpoints:
            print(f"\n📤 Checking: {endpoint}")
            response = self.session.get(f"{self.base_url}{endpoint}")
            self.print_response(response, f"Health Check - {endpoint}")
    
    def run_performance_test(self, num_requests=5):
        """Test performance with multiple requests"""
        print(f"\n⚡ Testing Performance ({num_requests} requests)...")
        
        start_time = time.time()
        responses = []
        
        for i in range(num_requests):
            print(f"📤 Request {i+1}/{num_requests}")
            response = self.session.post(
                f"{self.base_url}/chat",
                json={
                    "message": f"Performance test message {i+1}",
                    "session_id": f"perf-test-{i}"
                }
            )
            responses.append({
                "status": response.status_code,
                "time": time.time() - start_time
            })
        
        end_time = time.time()
        total_time = end_time - start_time
        avg_time = total_time / num_requests
        
        print(f"\n📊 Performance Results:")
        print(f"  Total time: {total_time:.2f}s")
        print(f"  Average per request: {avg_time:.2f}s")
        print(f"  Requests per second: {num_requests/total_time:.2f}")
        
        success_count = sum(1 for r in responses if r['status'] == 200)
        print(f"  Success rate: {success_count}/{num_requests} ({success_count/num_requests*100:.1f}%)")

def main():
    print("🤖 AI Agent Interactive Testing Suite")
    print("=====================================")
    
    # Check if server is running
    tester = AIAgentTester()
    try:
        response = requests.get(f"{tester.base_url}/health", timeout=5)
        if response.status_code != 200:
            print("❌ Server is not responding correctly")
            return
    except requests.exceptions.RequestException:
        print(f"❌ Cannot connect to server at {tester.base_url}")
        print("Make sure the server is running:")
        print("  python -m uvicorn src.api.main:app --reload")
        return
    
    print(f"✅ Server is running at {tester.base_url}")
    
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
        
        if test_type == "basic":
            tester.test_basic_chat()
        elif test_type == "rag":
            tester.test_rag_system()
        elif test_type == "tools":
            tester.test_mcp_tools()
        elif test_type == "eval":
            tester.test_evaluation_system()
        elif test_type == "context":
            tester.test_conversation_context()
        elif test_type == "health":
            tester.test_health_monitoring()
        elif test_type == "performance":
            tester.run_performance_test(10)
        elif test_type == "all":
            tester.test_basic_chat()
            tester.test_rag_system()
            tester.test_mcp_tools()
            tester.test_evaluation_system()
            tester.test_conversation_context()
            tester.test_health_monitoring()
            tester.run_performance_test(5)
        else:
            print(f"Unknown test type: {test_type}")
            print("Available tests: basic, rag, tools, eval, context, health, performance, all")
    else:
        # Interactive menu
        while True:
            print("\n🧪 Choose a test:")
            print("1. Basic Chat")
            print("2. RAG System") 
            print("3. MCP Tools")
            print("4. Evaluation System")
            print("5. Conversation Context")
            print("6. Health Monitoring")
            print("7. Performance Test")
            print("8. Run All Tests")
            print("9. Exit")
            
            choice = input("\nEnter choice (1-9): ").strip()
            
            if choice == "1":
                tester.test_basic_chat()
            elif choice == "2":
                tester.test_rag_system()
            elif choice == "3":
                tester.test_mcp_tools()
            elif choice == "4":
                tester.test_evaluation_system()
            elif choice == "5":
                tester.test_conversation_context()
            elif choice == "6":
                tester.test_health_monitoring()
            elif choice == "7":
                tester.run_performance_test(5)
            elif choice == "8":
                tester.test_basic_chat()
                tester.test_rag_system() 
                tester.test_mcp_tools()
                tester.test_evaluation_system()
                tester.test_conversation_context()
                tester.test_health_monitoring()
                tester.run_performance_test(5)
            elif choice == "9":
                break
            else:
                print("Invalid choice, please try again.")
    
    print("\n🎉 Testing completed!")

if __name__ == "__main__":
    main()