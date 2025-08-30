import streamlit as st
import os
from typing import Dict, Any
import time

from colligent_config import Config
from colligent_core import ContextAwareChatbot

# Page configuration
st.set_page_config(
    page_title="ColliGent",
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
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>You:</strong><br>
            {message['query']}
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
    
    # Header
    st.markdown('<h1 class="main-header">🤖 ColliGent</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center;">Hi, I\'m Collins! Ask me anything.</h3>', unsafe_allow_html=True)
    
    # Initialize chatbot
    initialize_chatbot()
    
    # Initialize global variables
    show_context = st.session_state.get('show_context', False)
    
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
        
        # Process user input
        if (user_input and send_button) or (user_input and st.session_state.get('auto_send', False)):
            if user_input.strip():
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
                    
                    # Add assistant response to history
                    assistant_message = {
                        'query': user_input,
                        'response': response['response'],
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
            ColliGent | Powered by RAG Technology
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
