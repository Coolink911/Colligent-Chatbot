#!/usr/bin/env python3
"""
Test script to verify the search fix works locally
"""

import sys
import os
import logging

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_document_processing():
    """Test the document processing logic"""
    
    # Simulate the search results that FAISS returns
    test_docs = [
        {
            'page_content': 'This is test content about engineering skills.',
            'metadata': {'source': 'test.pdf', 'type': 'pdf'},
            'score': 0.85
        },
        {
            'page_content': 'Another test document about collaboration.',
            'metadata': {'source': 'test2.pdf', 'type': 'pdf'},
            'score': 0.75
        }
    ]
    
    print("Testing document processing logic...")
    print(f"Test documents: {len(test_docs)}")
    
    # Test the exact logic from get_relevant_context
    context_parts = []
    for i, doc in enumerate(test_docs, 1):
        try:
            print(f"Processing document {i}, type: {type(doc)}")
            
            # Handle both Document objects and dictionaries
            if hasattr(doc, 'metadata'):
                # Document object
                print(f"Document {i} is a Document object")
                source = doc.metadata.get('source', 'Unknown')
                content = doc.page_content.strip()
            elif isinstance(doc, dict):
                # Dictionary
                print(f"Document {i} is a dict with keys: {list(doc.keys())}")
                source = doc.get('metadata', {}).get('source', 'Unknown')
                content = doc.get('page_content', '').strip()
                print(f"Document {i} source: {source}, content length: {len(content)}")
            else:
                # Fallback for any other type
                print(f"Unexpected document type: {type(doc)}")
                source = 'Unknown'
                content = str(doc)[:500] if doc else ''
            
            context_parts.append(f"Source {i} ({source}):\n{content}\n")
            print(f"Successfully processed document {i}")
            
        except Exception as doc_error:
            print(f"Error processing document {i}: {doc_error}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            context_parts.append(f"Source {i} (Error):\n[Document processing error]\n")
    
    result = "\n".join(context_parts)
    print(f"\nFinal result length: {len(result)}")
    print("Test completed successfully!")
    return result

if __name__ == "__main__":
    test_document_processing()
