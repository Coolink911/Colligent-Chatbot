#!/usr/bin/env python3
"""
ColliGent Startup Script
Quick launcher for the ColliGent Personal AI Assistant
"""

import os
import sys
import subprocess
import time

def print_banner():
    """Print the ColliGent banner"""
    print("""
🤖 ColliGent - Personal AI Assistant
=====================================
Powered by RAG Technology
    """)

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import streamlit
        import flask
        import langchain
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def run_streamlit():
    """Start the Streamlit web interface"""
    print("🚀 Starting ColliGent Web Interface...")
    print("📱 Access at: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "colligent_web_app.py", "--server.port", "8501"
        ])
    except KeyboardInterrupt:
        print("\n👋 ColliGent stopped")

def run_flask():
    """Start the Flask API server"""
    print("🚀 Starting ColliGent API Server...")
    print("🌐 Access at: http://localhost:5000")
    print("📚 API docs at: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "colligent_api_server.py"])
    except KeyboardInterrupt:
        print("\n👋 ColliGent stopped")

def main():
    """Main startup function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Show menu
    print("Choose your interface:")
    print("1. 🌐 Streamlit Web Interface (Recommended)")
    print("2. 🔌 Flask API Server")
    print("3. ❌ Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                run_streamlit()
                break
            elif choice == "2":
                run_flask()
                break
            elif choice == "3":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()
