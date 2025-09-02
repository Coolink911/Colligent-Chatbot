#!/usr/bin/env python3
"""
Simple test script to verify the app can run locally
"""

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing imports...")
    
    try:
        import streamlit as st
        print(f"✅ streamlit {st.__version__} imported successfully")
    except ImportError as e:
        print(f"❌ streamlit import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print(f"✅ pandas {pd.__version__} imported successfully")
    except ImportError as e:
        print(f"❌ pandas import failed: {e}")
        return False
    
    try:
        import os
        print("✅ os imported successfully")
    except ImportError as e:
        print(f"❌ os import failed: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality without Streamlit"""
    print("\nTesting basic functionality...")
    
    try:
        # Test file operations
        import os
        cwd = os.getcwd()
        files = os.listdir('.')
        print(f"✅ Current directory: {cwd}")
        print(f"✅ Files found: {len(files)}")
        
        # Test environment variables
        port = os.environ.get('PORT', 'Not set')
        python_version = os.environ.get('PYTHON_VERSION', 'Not set')
        print(f"✅ PORT: {port}")
        print(f"✅ PYTHON_VERSION: {python_version}")
        
        return True
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Colligent Test App Tests...\n")
    
    # Test imports
    imports_ok = test_imports()
    
    # Test basic functionality
    functionality_ok = test_basic_functionality()
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    
    if imports_ok and functionality_ok:
        print("🎉 All tests passed! The app should work locally.")
        print("\nTo run the test app locally:")
        print("streamlit run test_app.py --server.port=8501")
    else:
        print("❌ Some tests failed. Check the errors above.")
    
    print("="*50)

if __name__ == "__main__":
    main()
