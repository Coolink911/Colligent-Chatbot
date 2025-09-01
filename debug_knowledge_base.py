#!/usr/bin/env python3
"""
Debug script to check knowledge base status
Run this to see what's happening with document processing
"""

import os
import sys
import logging

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_data_folder():
    """Check if data folder exists and has files"""
    print("🔍 Checking data folder...")
    
    # Check current directory
    print(f"Current directory: {os.getcwd()}")
    print(f"Files in current directory: {os.listdir('.')}")
    
    # Check data folder
    data_folder = os.path.join(current_dir, "data")
    print(f"Looking for data folder at: {data_folder}")
    
    if os.path.exists(data_folder):
        print(f"✅ Data folder found!")
        files = os.listdir(data_folder)
        print(f"Files in data folder: {files}")
        
        # Check each file
        for file in files:
            file_path = os.path.join(data_folder, file)
            size = os.path.getsize(file_path)
            print(f"  📄 {file}: {size} bytes")
    else:
        print("❌ Data folder not found!")
        return False
    
    return True

def check_vector_db():
    """Check vector database status"""
    print("\n🔍 Checking vector database...")
    
    vector_db_path = os.path.join(current_dir, "vector_db")
    print(f"Vector DB path: {vector_db_path}")
    
    if os.path.exists(vector_db_path):
        print("✅ Vector DB folder exists!")
        files = os.listdir(vector_db_path)
        print(f"Files in vector DB: {files}")
    else:
        print("❌ Vector DB folder not found!")
        return False
    
    return True

def test_document_processing():
    """Test document processing"""
    print("\n🔍 Testing document processing...")
    
    try:
        from colligent_config import Config
        from colligent_document_processor import DocumentProcessor
        
        config = Config()
        processor = DocumentProcessor(config)
        
        print("✅ Document processor created successfully")
        
        # Process documents
        documents = processor.process_documents()
        print(f"📚 Processed {len(documents)} documents")
        
        if documents:
            print("Sample document:")
            print(f"  Content length: {len(documents[0]['content'])} characters")
            print(f"  Metadata: {documents[0]['metadata']}")
        
        return documents
        
    except Exception as e:
        print(f"❌ Error in document processing: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_vector_store():
    """Test vector store creation"""
    print("\n🔍 Testing vector store...")
    
    try:
        from colligent_config import Config
        from colligent_vector_db import VectorStore
        
        config = Config()
        vector_store = VectorStore(config)
        
        print("✅ Vector store created successfully")
        
        # Try to load existing store
        loaded = vector_store.load_vector_store()
        if loaded:
            print("✅ Existing vector store loaded")
        else:
            print("ℹ️ No existing vector store found")
        
        return vector_store
        
    except Exception as e:
        print(f"❌ Error in vector store: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_knowledge_base():
    """Test full knowledge base initialization"""
    print("\n🔍 Testing knowledge base initialization...")
    
    try:
        from colligent_config import Config
        from colligent_core import ContextAwareChatbot
        
        config = Config()
        chatbot = ContextAwareChatbot(config)
        
        print("✅ Chatbot created successfully")
        
        # Initialize knowledge base
        success = chatbot.initialize_knowledge_base()
        print(f"Knowledge base initialization: {'✅ Success' if success else '❌ Failed'}")
        
        if success:
            # Get info
            info = chatbot.get_knowledge_base_info()
            print(f"Knowledge base info: {info}")
        
        return success
        
    except Exception as e:
        print(f"❌ Error in knowledge base: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all diagnostic tests"""
    print("🚀 Colligent Knowledge Base Diagnostic")
    print("=" * 50)
    
    # Check data folder
    data_ok = check_data_folder()
    
    # Check vector DB
    vector_ok = check_vector_db()
    
    # Test document processing
    documents = test_document_processing()
    
    # Test vector store
    vector_store = test_vector_store()
    
    # Test full knowledge base
    kb_ok = test_knowledge_base()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 50)
    print(f"Data folder: {'✅ OK' if data_ok else '❌ FAILED'}")
    print(f"Vector DB: {'✅ OK' if vector_ok else '❌ FAILED'}")
    print(f"Document processing: {'✅ OK' if documents else '❌ FAILED'}")
    print(f"Vector store: {'✅ OK' if vector_store else '❌ FAILED'}")
    print(f"Knowledge base: {'✅ OK' if kb_ok else '❌ FAILED'}")
    
    if not kb_ok:
        print("\n🔧 RECOMMENDATIONS:")
        if not data_ok:
            print("  - Check that data folder exists and contains documents")
        if not documents:
            print("  - Document processing failed - check file formats and permissions")
        if not vector_store:
            print("  - Vector store creation failed - check dependencies")
        print("  - Try rebuilding knowledge base in the web app")

if __name__ == "__main__":
    main()
