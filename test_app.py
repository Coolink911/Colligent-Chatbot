import streamlit as st
import os

# Set page config
st.set_page_config(
    page_title="Colligent Test App",
    page_icon="🤖",
    layout="wide"
)

# Simple test app
def main():
    st.title("🤖 Colligent Test App")
    st.write("This is a simplified test version to debug deployment issues.")
    
    # Test basic functionality
    st.header("Basic Functionality Test")
    
    # Test session state
    if 'counter' not in st.session_state:
        st.session_state.counter = 0
    
    if st.button("Increment Counter"):
        st.session_state.counter += 1
    
    st.write(f"Counter: {st.session_state.counter}")
    
    # Test file operations
    st.header("File System Test")
    st.write(f"Current working directory: {os.getcwd()}")
    st.write(f"Files in current directory: {os.listdir('.')}")
    
    # Test environment variables
    st.header("Environment Variables Test")
    st.write(f"PORT: {os.environ.get('PORT', 'Not set')}")
    st.write(f"PYTHON_VERSION: {os.environ.get('PYTHON_VERSION', 'Not set')}")
    
    # Test imports
    st.header("Import Test")
    try:
        import pandas as pd
        st.success("✅ pandas imported successfully")
        st.write(f"pandas version: {pd.__version__}")
    except ImportError as e:
        st.error(f"❌ pandas import failed: {e}")
    
    try:
        import streamlit as st_lib
        st.success("✅ streamlit imported successfully")
        st.write(f"streamlit version: {st_lib.__version__}")
    except ImportError as e:
        st.error(f"❌ streamlit import failed: {e}")
    
    # Test simple chat interface
    st.header("Simple Chat Test")
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type a message..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Simulate assistant response
        response = f"Test response to: {prompt}"
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)

if __name__ == "__main__":
    main()
