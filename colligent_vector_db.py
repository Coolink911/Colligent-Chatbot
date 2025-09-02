import os
from typing import List, Dict, Any
import logging

# Set up logging first
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import Document type first (needed for type hints)
try:
    from langchain_core.documents import Document
except ImportError:
    # Fallback if langchain_core is not available
    Document = Any

# Initialize variables
CHROMADB_AVAILABLE = False
Chroma = Any

# Try to import chromadb and related modules
try:
    import chromadb
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import HuggingFaceEmbeddings
    CHROMADB_AVAILABLE = True
    logger.info("ChromaDB successfully imported")
except (ImportError, RuntimeError, Exception) as e:
    CHROMADB_AVAILABLE = False
    logger.warning(f"ChromaDB not available (error: {e}), will use fallback implementation")

# Create a function to check if ChromaDB is available
def is_chromadb_available():
    return CHROMADB_AVAILABLE

# Try to import config, but don't fail if it doesn't work
try:
    from colligent_config import Config
    logger.info("Successfully imported colligent_config")
except ImportError as e:
    logger.warning(f"Failed to import colligent_config: {e}, using fallback")
    # Create a minimal config class if import fails
    class Config:
        def __init__(self):
            # Don't use logger here to avoid dependency issues
            self.EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
            self.VECTOR_DB_PATH = "vector_db"
            self.DATA_FOLDER = "data"

class VectorStore:
    """Manages vector database operations for document storage and retrieval"""
    
    def __init__(self, config: Config):
        logger.info("Initializing VectorStore")
        chromadb_available = is_chromadb_available()
        logger.info(f"CHROMADB_AVAILABLE: {chromadb_available}")
        self.config = config
        
        # Initialize embeddings only if ChromaDB is available
        if chromadb_available:
            try:
                from langchain_community.embeddings import HuggingFaceEmbeddings
                logger.info(f"Creating embeddings with model: {config.EMBEDDING_MODEL}")
                self.embeddings = HuggingFaceEmbeddings(
                    model_name=config.EMBEDDING_MODEL,
                    model_kwargs={'device': 'cpu'}
                )
                logger.info("Embeddings created successfully")
            except Exception as e:
                logging.error(f"Failed to initialize embeddings: {e}")
                # Don't modify global variable, just set local embeddings to None
                self.embeddings = None
        else:
            logger.info("ChromaDB not available, setting embeddings to None")
            self.embeddings = None
            
        self.vector_db = None
        self.collection_name = "documents"
        logger.info("VectorStore initialization complete")
    
    def create_vector_store(self, documents: List[Any]):
        """Create a new vector store from documents"""
        if not documents:
            logger.warning("No documents provided for vector store creation")
            return None
        
        if not is_chromadb_available():
            logger.warning("ChromaDB not available, cannot create vector store")
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
    
    def load_vector_store(self):
        """Load existing vector store"""
        if not is_chromadb_available():
            logger.warning("ChromaDB not available, cannot load vector store")
            return None
            
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
    
    def search_similar(self, query: str, k: int = 5) -> List[Any]:
        """Search for similar documents"""
        if not is_chromadb_available():
            logger.warning("ChromaDB not available, using fallback search")
            return self._fallback_search(query, k)
            
        if not self.vector_db:
            logger.error("Vector store not initialized")
            return []
        
        try:
            results = self.vector_db.similarity_search(query, k=k)
            logger.info(f"Found {len(results)} similar documents for query: {query[:50]}...")
            return results
        except Exception as e:
            logger.error(f"Error searching vector store: {str(e)}")
            return self._fallback_search(query, k)
    
    def _fallback_search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Fallback search when ChromaDB is not available"""
        logger.info("Using fallback search implementation")
        # Return empty results for now - this will be handled by the core
        return []
    
    def search_with_score(self, query: str, k: int = 5) -> List[tuple]:
        """Search for similar documents with similarity scores"""
        if not is_chromadb_available():
            logger.warning("ChromaDB not available, using fallback search")
            return []
            
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
        if not is_chromadb_available():
            return {
                "collection_name": "fallback_documents",
                "document_count": 0,
                "embedding_model": "fallback",
                "index_type": "FAISS"
            }
        
        if not self.vector_db:
            return {"error": "Vector store not initialized"}
        
        try:
            collection = self.vector_db._collection
            count = collection.count()
            return {
                "collection_name": self.collection_name,
                "document_count": count,
                "embedding_model": self.config.EMBEDDING_MODEL,
                "index_type": "ChromaDB"
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
