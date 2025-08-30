import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the chatbot agent"""
    
    # OpenAI API Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # Vector Database Configuration
    VECTOR_DB_PATH = "vector_db"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # Document Processing
    DATA_FOLDER = "data"
    SUPPORTED_FORMATS = [".pdf", ".txt", ".docx"]
    
    # Chatbot Configuration
    MAX_TOKENS = 1500
    TEMPERATURE = 0.7
    
    # Security Configuration
    ENABLE_RATE_LIMITING = True
    MAX_REQUESTS_PER_MINUTE = 20  # Reduced for better security
    SESSION_TIMEOUT_MINUTES = 30   # Shorter timeout
    ENABLE_INPUT_VALIDATION = True
    MAX_INPUT_LENGTH = 500         # Reduced for security
    ENABLE_AUTHENTICATION = True
    ALLOWED_IPS = ["127.0.0.1", "localhost", "192.168.1.149"]  # Restrict access
    ENABLE_LOGGING = True
    LOG_SUSPICIOUS_ACTIVITY = True
    
    # Embedding Model
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    
    # System Prompt
    SYSTEM_PROMPT = """You are Collins Maripane's personal AI assistant. You speak in Collins' voice and refer to the materials as Collins' own documents and experiences. 

    When answering questions:
    - Use "I" and "my" to refer to Collins' experiences, skills, and background
    - Reference the documents as "my CV", "my research", "my work", etc.
    - Be personal and authentic to Collins' voice and style
    - Base all answers on the information in Collins' documents
    - If the context doesn't contain enough information to answer the question, respond with: "I do not have available information yet."
    - Be concise but thorough in your responses
    - Maintain Collins' professional yet approachable tone"""
