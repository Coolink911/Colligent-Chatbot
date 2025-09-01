# Colligent Package Initialization
# This file makes the directory a proper Python package

__version__ = "1.0.0"
__author__ = "Collins Maripane"

# Import main components for easier access
try:
    from .colligent_config import Config
    from .colligent_core import ContextAwareChatbot
    from .colligent_document_processor import DocumentProcessor
    from .colligent_vector_db import VectorDatabase
except ImportError:
    # Fallback for direct imports
    pass
