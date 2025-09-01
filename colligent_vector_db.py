import os
import chromadb
from typing import List, Dict, Any
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
import logging

# Import handling for both local and cloud deployment
import sys
import os

# Add current directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from colligent_config import Config
except ImportError as e:
    raise ImportError(f"Could not import colligent_config: {e}")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorStore:
    """Manages vector database operations for document storage and retrieval"""
    
    def __init__(self, config: Config):
        self.config = config
        self.embeddings = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'}
        )
        self.vector_db = None
        self.collection_name = "documents"
    
    def create_vector_store(self, documents: List[Document]) -> Chroma:
        """Create a new vector store from documents"""
        if not documents:
            logger.warning("No documents provided for vector store creation")
            return None
        
        try:
            # Create vector store directory if it doesn't exist
            os.makedirs(self.config.VECTOR_DB_PATH, exist_ok=True)
            
            # Create the vector store
            vector_db = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=self.config.VECTOR_DB_PATH,
                collection_name=self.collection_name
            )
            
            # Vector store is automatically persisted in Chroma 0.4.x+
            
            logger.info(f"Created vector store with {len(documents)} documents")
            self.vector_db = vector_db
            return vector_db
            
        except Exception as e:
            logger.error(f"Error creating vector store: {str(e)}")
            return None
    
    def load_vector_store(self) -> Chroma:
        """Load existing vector store"""
        try:
            if os.path.exists(self.config.VECTOR_DB_PATH):
                vector_db = Chroma(
                    persist_directory=self.config.VECTOR_DB_PATH,
                    embedding_function=self.embeddings,
                    collection_name=self.collection_name
                )
                logger.info("Loaded existing vector store")
                self.vector_db = vector_db
                return vector_db
            else:
                logger.info("No existing vector store found")
                return None
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
            return None
    
    def search_similar(self, query: str, k: int = 5) -> List[Document]:
        """Search for similar documents"""
        if not self.vector_db:
            logger.error("Vector store not initialized")
            return []
        
        try:
            results = self.vector_db.similarity_search(query, k=k)
            logger.info(f"Found {len(results)} similar documents for query: {query[:50]}...")
            return results
        except Exception as e:
            logger.error(f"Error searching vector store: {str(e)}")
            return []
    
    def search_with_score(self, query: str, k: int = 5) -> List[tuple]:
        """Search for similar documents with similarity scores"""
        if not self.vector_db:
            logger.error("Vector store not initialized")
            return []
        
        try:
            results = self.vector_db.similarity_search_with_score(query, k=k)
            logger.info(f"Found {len(results)} similar documents with scores for query: {query[:50]}...")
            return results
        except Exception as e:
            logger.error(f"Error searching vector store with scores: {str(e)}")
            return []
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the vector store collection"""
        if not self.vector_db:
            return {"error": "Vector store not initialized"}
        
        try:
            collection = self.vector_db._collection
            count = collection.count()
            return {
                "collection_name": self.collection_name,
                "document_count": count,
                "embedding_model": self.config.EMBEDDING_MODEL
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {str(e)}")
            return {"error": str(e)}
    
    def delete_vector_store(self):
        """Delete the vector store"""
        try:
            import shutil
            if os.path.exists(self.config.VECTOR_DB_PATH):
                shutil.rmtree(self.config.VECTOR_DB_PATH)
                logger.info("Deleted vector store")
                self.vector_db = None
        except Exception as e:
            logger.error(f"Error deleting vector store: {str(e)}")
