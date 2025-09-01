#!/usr/bin/env python3
"""
Test script to verify all imports work correctly
Run this before deploying to catch import issues
"""

import sys
import os

print("🧪 Testing Colligent imports...")
print("=" * 40)

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Test imports one by one
try:
    print("✅ Testing colligent_config import...")
    from colligent_config import Config
    print("   ✓ Config imported successfully")
except ImportError as e:
    print(f"   ❌ Failed to import colligent_config: {e}")
    sys.exit(1)

try:
    print("✅ Testing colligent_document_processor import...")
    from colligent_document_processor import DocumentProcessor
    print("   ✓ DocumentProcessor imported successfully")
except ImportError as e:
    print(f"   ❌ Failed to import colligent_document_processor: {e}")
    sys.exit(1)

try:
    print("✅ Testing colligent_vector_db import...")
    from colligent_vector_db import VectorStore
    print("   ✓ VectorStore imported successfully")
except ImportError as e:
    print(f"   ❌ Failed to import colligent_vector_db: {e}")
    sys.exit(1)

try:
    print("✅ Testing colligent_core import...")
    from colligent_core import ContextAwareChatbot
    print("   ✓ ContextAwareChatbot imported successfully")
except ImportError as e:
    print(f"   ❌ Failed to import colligent_core: {e}")
    sys.exit(1)

try:
    print("✅ Testing streamlit import...")
    import streamlit as st
    print("   ✓ Streamlit imported successfully")
except ImportError as e:
    print(f"   ❌ Failed to import streamlit: {e}")
    sys.exit(1)

print("\n🎉 All imports successful! Ready for deployment.")
print("=" * 40)
