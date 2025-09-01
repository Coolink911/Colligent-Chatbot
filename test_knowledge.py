#!/usr/bin/env python3
"""
Test script to verify knowledge base is working
"""

import os
import sys

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def test_knowledge_base():
    """Test if knowledge base is working"""
    try:
        from colligent_config import Config
        from colligent_core import ContextAwareChatbot
        
        print("🚀 Testing Colligent Knowledge Base")
        print("=" * 40)
        
        # Create chatbot
        config = Config()
        chatbot = ContextAwareChatbot(config)
        
        # Initialize knowledge base
        print("📚 Initializing knowledge base...")
        success = chatbot.initialize_knowledge_base()
        
        if not success:
            print("❌ Failed to initialize knowledge base")
            return False
        
        # Get info
        info = chatbot.get_knowledge_base_info()
        print(f"✅ Knowledge base info: {info}")
        
        # Test questions
        test_questions = [
            "What kind of engineer am I?",
            "What are my strongest technical skills?",
            "What projects am I most proud of?",
            "What is my research about?"
        ]
        
        print("\n🧪 Testing Questions:")
        print("=" * 40)
        
        for question in test_questions:
            print(f"\n❓ Question: {question}")
            response = chatbot.ask_question(question)
            print(f"🤖 Response: {response['response'][:200]}...")
            
            if "do not have available information" in response['response'].lower():
                print("⚠️  WARNING: No information found!")
            else:
                print("✅ SUCCESS: Found relevant information!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_knowledge_base()
    if success:
        print("\n🎉 Knowledge base test completed successfully!")
    else:
        print("\n💥 Knowledge base test failed!")
