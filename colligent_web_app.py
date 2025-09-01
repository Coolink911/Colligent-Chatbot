import streamlit as st
import os
from typing import Dict, Any
import time

# Import handling for both local and cloud deployment
import sys
import os

# Add current directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from colligent_config import Config
    from colligent_core import ContextAwareChatbot
except ImportError as e:
    st.error(f"Import Error: {e}")
    st.error("Please check that all required files are present in the repository.")
    st.stop()
import re
import time
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Collins' Personal AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #1f77b4;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left-color: #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left-color: #9c27b0;
    }
    .source-info {
        font-size: 0.8rem;
        color: #666;
        font-style: italic;
        margin-top: 0.5rem;
    }
    .left-panel {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .status-card {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        margin-bottom: 1rem;
    }
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
    }
    .quick-question-btn {
        background-color: #e3f2fd;
        border: 1px solid #2196f3;
        color: #1976d2;
    }
    .quick-question-btn:hover {
        background-color: #bbdefb;
    }
</style>
""", unsafe_allow_html=True)

# Security functions
def validate_input(text: str, max_length: int = 1000) -> bool:
    """Validate user input for security"""
    if not text or len(text.strip()) == 0:
        return False
    
    if len(text) > max_length:
        return False
    
    # Check for potentially harmful patterns
    harmful_patterns = [
        r'<script.*?>.*?</script>',
        r'<iframe.*?>.*?</iframe>',
        r'javascript:',
        r'data:text/html',
        r'vbscript:',
        r'onload=',
        r'onerror=',
        r'onclick='
    ]
    
    for pattern in harmful_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    
    return True

def check_rate_limit(user_id: str = "default") -> bool:
    """Check if user has exceeded rate limit"""
    if 'rate_limit' not in st.session_state:
        st.session_state.rate_limit = {}
    
    current_time = time.time()
    user_requests = st.session_state.rate_limit.get(user_id, [])
    
    # Remove requests older than 1 minute
    user_requests = [req_time for req_time in user_requests if current_time - req_time < 60]
    
    # Check if user has exceeded limit (30 requests per minute)
    if len(user_requests) >= 30:
        return False
    
    # Add current request
    user_requests.append(current_time)
    st.session_state.rate_limit[user_id] = user_requests
    
    return True

def sanitize_output(text: str) -> str:
    """Sanitize output to prevent XSS"""
    # Remove potentially harmful HTML tags
    text = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<iframe.*?>.*?</iframe>', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
    text = re.sub(r'data:text/html', '', text, flags=re.IGNORECASE)
    
    return text

def check_ip_whitelist() -> bool:
    """Check if client IP is in whitelist"""
    config = Config()
    allowed_ips = config.ALLOWED_IPS
    
    # Get client IP (works with proxy)
    client_ip = st.experimental_get_query_params().get('client_ip', [None])[0]
    if not client_ip:
        # Try to get from headers
        client_ip = "127.0.0.1"  # Default for local development
    
    return client_ip in allowed_ips or "localhost" in allowed_ips

def log_suspicious_activity(action: str, details: str = ""):
    """Log suspicious activity"""
    config = Config()
    if config.LOG_SUSPICIOUS_ACTIVITY:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] SUSPICIOUS: {action} - {details}"
        print(log_entry)  # In production, use proper logging

def initialize_chatbot():
    """Initialize the chatbot"""
    if 'chatbot' not in st.session_state:
        config = Config()
        st.session_state.chatbot = ContextAwareChatbot(config)
        
        # Initialize knowledge base
        with st.spinner("Initializing knowledge base..."):
            success = st.session_state.chatbot.initialize_knowledge_base()
            if success:
                st.success("Knowledge base initialized successfully!")
            else:
                st.error("Failed to initialize knowledge base. Please check your documents.")

def display_chat_message(message: Dict[str, Any], is_user: bool = False):
    """Display a chat message"""
    if is_user:
        # Sanitize user input
        safe_query = sanitize_output(message['query'])
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>You:</strong><br>
            {safe_query}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>Assistant:</strong><br>
            {message['response']}
        </div>
        """, unsafe_allow_html=True)
        
        # Display sources if available
        if 'sources' in message and message['sources']:
            sources_text = ", ".join(message['sources'])
            st.markdown(f"""
            <div class="source-info">
                📚 Sources: {sources_text}
            </div>
            """, unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Security checks
    config = Config()
    
    # IP whitelist check
    if config.ENABLE_AUTHENTICATION and not check_ip_whitelist():
        st.error("🚫 Access denied. Your IP is not authorized to access this application.")
        st.stop()
    
    # Session timeout check
    if 'last_activity' in st.session_state:
        last_activity = st.session_state.last_activity
        timeout_minutes = config.SESSION_TIMEOUT_MINUTES
        if datetime.now() - last_activity > timedelta(minutes=timeout_minutes):
            st.error("⏰ Session expired. Please refresh the page.")
            st.stop()
    
    # Update last activity
    st.session_state.last_activity = datetime.now()
    
    # Header
    st.markdown('<h1 class="main-header">🤖 ColliGent</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center;">Hi, I\'m Collins! Ask me anything.</h3>', unsafe_allow_html=True)
    
    # Initialize chatbot
    initialize_chatbot()
    
    # Main layout with left panel and chat area
    col1, col2 = st.columns([1, 3])
    
    # Initialize global variables
    show_context = st.session_state.get('show_context', False)
    
    # Left panel for interactive buttons and settings
    with col1:
        # Initialize session state for button states
        if 'show_system_status' not in st.session_state:
            st.session_state.show_system_status = False
        if 'show_settings' not in st.session_state:
            st.session_state.show_settings = False
        if 'show_rag_info' not in st.session_state:
            st.session_state.show_rag_info = False
        if 'show_help' not in st.session_state:
            st.session_state.show_help = False
        
        # System Status Button
        if st.button("System Status", type="primary", key="system_status_btn"):
            st.session_state.show_system_status = not st.session_state.show_system_status
            st.rerun()
        
        if st.session_state.show_system_status:
            if 'chatbot' in st.session_state:
                kb_info = st.session_state.chatbot.get_knowledge_base_info()
                if 'error' not in kb_info:
                    st.success("✅ Knowledge Base Loaded")
                    st.info(f"📚 Documents: {kb_info.get('document_count', 0)}")
                    st.info(f"🔧 Model: {kb_info.get('embedding_model', 'N/A')}")
                else:
                    st.error(f"❌ Error: {kb_info['error']}")
        
        # Settings Button
        if st.button("Settings", type="primary", key="settings_btn"):
            st.session_state.show_settings = not st.session_state.show_settings
            st.rerun()
        
        if st.session_state.show_settings:
            # API Key input
            api_key = st.text_input(
                "OpenAI API Key (optional)",
                type="password",
                help="Enter your OpenAI API key for better responses"
            )
            
            if api_key and api_key != st.session_state.get('api_key', ''):
                st.session_state.api_key = api_key
                os.environ['OPENAI_API_KEY'] = api_key
                # Reinitialize chatbot with new API key
                config = Config()
                st.session_state.chatbot = ContextAwareChatbot(config)
                st.success("API key updated!")
            
            # Show context option
            show_context = st.checkbox("Show context in responses", value=st.session_state.get('show_context', False))
            st.session_state.show_context = show_context
        
        # RAG Information Button
        if st.button("RAG System Info", type="primary", key="rag_info_btn"):
            st.session_state.show_rag_info = not st.session_state.show_rag_info
            st.rerun()
        
        if st.session_state.show_rag_info:
            st.markdown("### 🔄 RAG Components")
            st.markdown("""
            - ✅ **Retrieval**: Active
            - ✅ **Generation**: Active  
            - ✅ **Fallback**: Available
            """)
            
            st.markdown("### 📊 How RAG Works")
            st.info("""
            **Retrieval-Augmented Generation (RAG) System:**
            
            1. **🔍 Search**: I search through my CV and research documents
            2. **🧠 Think**: I combine the relevant information from my materials  
            3. **📚 Sources**: I show you which of my documents I used for each answer
            
            This ensures my answers are based on my actual experiences and work, not just general knowledge.
            """)
        
        # Help & Actions Button
        if st.button("Help & Actions", type="primary", key="help_btn"):
            st.session_state.show_help = not st.session_state.show_help
            st.rerun()
        
        if st.session_state.show_help:
            # Clear conversation button
            if st.button("🗑️ Clear Chat", type="secondary", key="clear_chat_btn"):
                if 'chatbot' in st.session_state:
                    st.session_state.chatbot.clear_conversation_history()
                st.session_state.messages = []
                st.rerun()
            
            # Rebuild knowledge base button
            if st.button("🔄 Rebuild KB", type="secondary", key="rebuild_kb_btn"):
                with st.spinner("Rebuilding knowledge base..."):
                    success = st.session_state.chatbot.initialize_knowledge_base(force_rebuild=True)
                    if success:
                        st.success("Knowledge base rebuilt!")
                    else:
                        st.error("Failed to rebuild knowledge base.")
                st.rerun()
            
            # Quick tips
            st.markdown("### 💡 Quick Tips")
            st.markdown("""
            - **Ask about my research**: "What is your diffusion model research about?"
            - **Ask about my skills**: "What programming languages do you know?"
            - **Ask about my background**: "Tell me about your education and experience"
            - **Use different modes**: Try Code Style mode for technical details!
            """)
    
    # Main chat area
    with col2:
        # Initialize messages in session state
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        # Mode selection with icons and descriptions (moved to bottom)
        mode_options = {
            "default": {"icon": "💬", "name": "Default", "desc": "Natural conversational tone"},
            "interview": {"icon": "👔", "name": "Interview", "desc": "Professional & concise"},
            "storytelling": {"icon": "📖", "name": "Storytelling", "desc": "Narrative & reflective"},
            "fast_facts": {"icon": "⚡", "name": "Fast Facts", "desc": "Bullet points & TL;DR"},
            "humble_brag": {"icon": "💪", "name": "Humble Brag", "desc": "Confident self-promotion"},
            "code_style": {"icon": "💻", "name": "Code Style", "desc": "Technical & implementation-focused"}
        }
        
        # Quick Questions
        st.markdown("### 💡 Quick Questions")
        st.markdown("*Click any question to get started*")
        
        # First row - Professional questions
        qcol1, qcol2, qcol3 = st.columns(3)
        
        with qcol1:
            if st.button("What kind of engineer am I?", key="q1"):
                # Process the question directly
                user_message = {
                    'query': "What kind of engineer am I?",
                    'is_user': True
                }
                st.session_state.messages.append(user_message)
                
                with st.spinner("Thinking..."):
                    response = st.session_state.chatbot.ask_question(
                        "What kind of engineer am I?", 
                        include_context=show_context
                    )
                    
                    assistant_message = {
                        'query': "What kind of engineer am I?",
                        'response': response['response'],
                        'sources': response.get('sources', []),
                        'is_user': False
                    }
                    st.session_state.messages.append(assistant_message)
                st.rerun()
        
        with qcol2:
            if st.button("What are my strongest technical skills?", key="q2"):
                # Process the question directly
                user_message = {
                    'query': "What are my strongest technical skills?",
                    'is_user': True
                }
                st.session_state.messages.append(user_message)
                
                with st.spinner("Thinking..."):
                    response = st.session_state.chatbot.ask_question(
                        "What are my strongest technical skills?", 
                        include_context=show_context
                    )
                    
                    assistant_message = {
                        'query': "What are my strongest technical skills?",
                        'response': response['response'],
                        'sources': response.get('sources', []),
                        'is_user': False
                    }
                    st.session_state.messages.append(assistant_message)
                st.rerun()
        
        with qcol3:
            if st.button("What projects am I most proud of?", key="q3"):
                # Process the question directly
                user_message = {
                    'query': "What projects am I most proud of?",
                    'is_user': True
                }
                st.session_state.messages.append(user_message)
                
                with st.spinner("Thinking..."):
                    response = st.session_state.chatbot.ask_question(
                        "What projects am I most proud of?", 
                        include_context=show_context
                    )
                    
                    assistant_message = {
                        'query': "What projects am I most proud of?",
                        'response': response['response'],
                        'sources': response.get('sources', []),
                        'is_user': False
                    }
                    st.session_state.messages.append(assistant_message)
                st.rerun()
        
        # Second row - Self-reflective questions
        st.markdown("### 🤔 Self-Reflection Questions")
        rcol1, rcol2, rcol3 = st.columns(3)
        
        with rcol1:
            if st.button("What energizes or drains me?", key="r1"):
                # Process the question directly
                user_message = {
                    'query': "What kind of tasks energize or drain me?",
                    'is_user': True
                }
                st.session_state.messages.append(user_message)
                
                with st.spinner("Reflecting..."):
                    response = st.session_state.chatbot.ask_question(
                        "What kind of tasks energize or drain me?", 
                        include_context=show_context
                    )
                    
                    assistant_message = {
                        'query': "What kind of tasks energize or drain me?",
                        'response': response['response'],
                        'sources': response.get('sources', []),
                        'is_user': False
                    }
                    st.session_state.messages.append(assistant_message)
                st.rerun()
        
        with rcol2:
            if st.button("How do I collaborate best?", key="r2"):
                # Process the question directly
                user_message = {
                    'query': "How do I collaborate best with others?",
                    'is_user': True
                }
                st.session_state.messages.append(user_message)
                
                with st.spinner("Reflecting..."):
                    response = st.session_state.chatbot.ask_question(
                        "How do I collaborate best with others?", 
                        include_context=show_context
                    )
                    
                    assistant_message = {
                        'query': "How do I collaborate best with others?",
                        'response': response['response'],
                        'sources': response.get('sources', []),
                        'is_user': False
                    }
                    st.session_state.messages.append(assistant_message)
                st.rerun()
        
        with rcol3:
            if st.button("Where do I need to grow?", key="r3"):
                # Process the question directly
                user_message = {
                    'query': "Where do I need to grow?",
                    'is_user': True
                }
                st.session_state.messages.append(user_message)
                
                with st.spinner("Reflecting..."):
                    response = st.session_state.chatbot.ask_question(
                        "Where do I need to grow?", 
                        include_context=show_context
                    )
                    
                    assistant_message = {
                        'query': "Where do I need to grow?",
                        'response': response['response'],
                        'sources': response.get('sources', []),
                        'is_user': False
                    }
                    st.session_state.messages.append(assistant_message)
                st.rerun()
        
        # Display chat history
        for message in st.session_state.messages:
            display_chat_message(message, is_user=message.get('is_user', False))
        
        # Chat input with mode indicator
        with st.container():
            # Get current mode
            current_mode = st.session_state.chatbot.get_current_mode()
            current_mode_info = mode_options.get(current_mode, {})
            
            # Chat input area
            input_col1, input_col2 = st.columns([4, 1])
            
            with input_col1:
                user_input = st.text_input(
                    f"Ask me anything (responding in {current_mode_info.get('name', 'Default')} mode)...",
                    key="user_input",
                    placeholder="e.g., What is the main topic of my research?"
                )
            
            with input_col2:
                send_button = st.button("Send", type="primary")
            
            # Response Mode Selection (ChatGPT-style at bottom)
            st.markdown("---")
            st.markdown("### 🎭 Response Mode")
            st.markdown("*Choose how I should respond to your questions*")
            
            # Create mode selection buttons in a horizontal row
            mode_cols = st.columns(6)
            
            for idx, (mode_key, mode_info) in enumerate(mode_options.items()):
                with mode_cols[idx]:
                    # Create a styled button for each mode
                    button_text = f"{mode_info['icon']} {mode_info['name']}"
                    is_selected = mode_key == current_mode
                    
                    # Use different button styles for selected vs unselected
                    if is_selected:
                        if st.button(f"✅ {mode_info['name']}", key=f"bottom_mode_{mode_key}", type="primary"):
                            pass  # Already selected
                    else:
                        if st.button(mode_info['name'], key=f"bottom_mode_{mode_key}", type="secondary"):
                            result = st.session_state.chatbot.set_mode(mode_key)
                            st.success(f"Mode switched to: {mode_info['name']}")
                            st.rerun()
                    
                    # Show description as tooltip
                    st.caption(f"_{mode_info['desc']}_")
        
        # Process user input with security checks
        if (user_input and send_button) or (user_input and st.session_state.get('auto_send', False)):
            if user_input.strip():
                # Security validation
                if not validate_input(user_input):
                    st.error("❌ Invalid input detected. Please check your message and try again.")
                    st.rerun()
                
                # Rate limiting check
                if not check_rate_limit():
                    st.error("⚠️ Rate limit exceeded. Please wait a moment before sending another message.")
                    st.rerun()
                
                # Add user message to history
                user_message = {
                    'query': user_input,
                    'is_user': True
                }
                st.session_state.messages.append(user_message)
                
                # Get chatbot response
                with st.spinner("Thinking..."):
                    response = st.session_state.chatbot.ask_question(
                        user_input, 
                        include_context=show_context
                    )
                    
                    # Sanitize response
                    safe_response = sanitize_output(response['response'])
                    
                    # Add assistant response to history
                    assistant_message = {
                        'query': user_input,
                        'response': safe_response,
                        'sources': response.get('sources', []),
                        'is_user': False
                    }
                    st.session_state.messages.append(assistant_message)
                
                # Use form_submit_button to clear input properly
                st.rerun()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.8rem;">
            Collins' Personal AI Assistant | Powered by RAG Technology
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
