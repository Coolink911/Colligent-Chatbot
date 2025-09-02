import streamlit as st
import os

st.set_page_config(
    page_title="Simple Test App",
    page_icon="🚀",
    layout="wide"
)

def main():
    st.title("🚀 Simple Test App")
    st.write("This is a minimal test app to verify deployment works!")
    
    # Basic functionality test
    st.header("✅ Basic Tests")
    
    # Counter
    if 'counter' not in st.session_state:
        st.session_state.counter = 0
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Click Me!"):
            st.session_state.counter += 1
        st.write(f"Counter: {st.session_state.counter}")
    
    with col2:
        st.write("✅ Session state working")
    
    # Environment info
    st.header("🌍 Environment Info")
    st.write(f"**Current Directory:** {os.getcwd()}")
    st.write(f"**Files Found:** {len(os.listdir('.'))}")
    st.write(f"**PORT:** {os.environ.get('PORT', 'Not set')}")
    st.write(f"**Python Version:** {os.environ.get('PYTHON_VERSION', 'Not set')}")
    
    # Import test
    st.header("📦 Import Test")
    try:
        import streamlit as st_lib
        st.success(f"✅ Streamlit {st_lib.__version__} imported successfully")
    except Exception as e:
        st.error(f"❌ Streamlit import failed: {e}")
    
    # Simple chat
    st.header("💬 Simple Chat")
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Display messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Say something..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Simple response
        response = f"Echo: {prompt}"
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.write(response)
    
    # Success message
    st.success("🎉 If you can see this, the app is working perfectly!")

if __name__ == "__main__":
    main()
