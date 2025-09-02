import os
import logging
import sys
from typing import List, Dict, Any, Optional

# Set up logging at the very top
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize fallback variables at module level
CHROMADB_AVAILABLE = False
Chroma = Any

try:
    import chromadb
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_core.documents import Document
    CHROMADB_AVAILABLE = True
    logger.info("ChromaDB successfully imported")
except ImportError as e:
    logger.warning(f"ChromaDB import failed: {e}")
    CHROMADB_AVAILABLE = False
    Chroma = Any

def is_chromadb_available():
    """Check if ChromaDB is available"""
    return CHROMADB_AVAILABLE

class VectorStore:
    """Vector database operations with robust fallback system"""
    
    def __init__(self, config):
        self.config = config
        self.embeddings = None
        self.vector_db = None
        self.fallback_docs = []
        
        try:
            if CHROMADB_AVAILABLE:
                logger.info("Initializing VectorStore with ChromaDB")
                self.embeddings = HuggingFaceEmbeddings(
                    model_name=self.config.EMBEDDING_MODEL
                )
                logger.info("Embeddings created successfully")
            else:
                logger.warning("ChromaDB not available, using fallback mode")
                self._setup_fallback()
        except Exception as e:
            logger.error(f"Error initializing embeddings: {e}")
            self._setup_fallback()
    
    def _setup_fallback(self):
        """Setup fallback document storage"""
        logger.info("Setting up fallback document storage")
        self.fallback_docs = []
    
    def create_vector_store(self, documents: List[Document]) -> bool:
        """Create vector store with robust fallback"""
        try:
            if not CHROMADB_AVAILABLE:
                logger.warning("ChromaDB not available, using fallback storage")
                return self._fallback_create_store(documents)
            
            if not documents:
                logger.error("No documents provided for vector store creation")
                return False
            
            logger.info(f"Creating ChromaDB vector store with {len(documents)} documents")
            
            # Create ChromaDB vector store
            vector_db = Chroma(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=self.config.VECTOR_DB_PATH
            )
            
            # Persist the vector store
            vector_db.persist()
            
            self.vector_db = vector_db
            logger.info("ChromaDB vector store created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create ChromaDB vector store: {e}")
            logger.info("Falling back to simple document storage")
            return self._fallback_create_store(documents)
    
    def _fallback_create_store(self, documents: List[Document]) -> bool:
        """Fallback storage when ChromaDB fails"""
        try:
            logger.info(f"Creating fallback storage with {len(documents)} documents")
            self.fallback_docs = documents
            logger.info("Fallback storage created successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to create fallback storage: {e}")
            return False
    
    def load_vector_store(self) -> bool:
        """Load existing vector store with fallback"""
        try:
            if not CHROMADB_AVAILABLE:
                logger.info("ChromaDB not available, checking fallback storage")
                return len(self.fallback_docs) > 0
            
            if not os.path.exists(self.config.VECTOR_DB_PATH):
                logger.info("No existing vector store found")
                return False
            
            logger.info("Loading existing ChromaDB vector store")
            self.vector_db = Chroma(
                persist_directory=self.config.VECTOR_DB_PATH,
                embedding_function=self.embeddings
            )
            logger.info("Existing vector store loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error loading existing vector store: {e}")
            logger.info("Falling back to simple storage")
            return len(self.fallback_docs) > 0
    
    def search_similar(self, query: str, k: int = 5) -> List[Document]:
        """Search for similar documents with fallback"""
        try:
            if CHROMADB_AVAILABLE and self.vector_db:
                logger.info(f"Searching ChromaDB for: {query[:50]}...")
                results = self.vector_db.similarity_search(query, k=k)
                logger.info(f"Found {len(results)} similar documents")
                return results
            else:
                logger.info("Using fallback search")
                return self._fallback_search(query, k)
                
        except Exception as e:
            logger.error(f"Error in similarity search: {e}")
            logger.info("Using fallback search due to error")
            return self._fallback_search(query, k)
    
    def _fallback_search(self, query: str, k: int = 5) -> List[Document]:
        """Simple fallback search when vector search fails"""
        try:
            if not self.fallback_docs:
                logger.warning("No documents available for fallback search")
                return []
            
            # Simple keyword-based search as fallback
            query_lower = query.lower()
            relevant_docs = []
            
            for doc in self.fallback_docs:
                content_lower = doc.page_content.lower()
                # Check if query words appear in document
                query_words = query_lower.split()
                relevance_score = sum(1 for word in query_words if word in content_lower)
                
                if relevance_score > 0:
                    relevant_docs.append((doc, relevance_score))
            
            # Sort by relevance and return top k
            relevant_docs.sort(key=lambda x: x[1], reverse=True)
            results = [doc for doc, score in relevant_docs[:k]]
            
            logger.info(f"Fallback search found {len(results)} relevant documents")
            return results
            
        except Exception as e:
            logger.error(f"Error in fallback search: {e}")
            return []
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get collection information with fallback"""
        try:
            if CHROMADB_AVAILABLE and self.vector_db:
                # Try to get ChromaDB collection info
                try:
                    collection = self.vector_db._collection
                    return {
                        'collection_name': collection.name,
                        'document_count': collection.count(),
                        'embedding_model': self.config.EMBEDDING_MODEL,
                        'index_type': 'ChromaDB'
                    }
                except Exception as e:
                    logger.warning(f"Could not get ChromaDB collection info: {e}")
                    return self._fallback_collection_info()
            else:
                return self._fallback_collection_info()
                
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return self._fallback_collection_info()
    
    def _fallback_collection_info(self) -> Dict[str, Any]:
        """Fallback collection information"""
        return {
            'collection_name': 'fallback_documents',
            'document_count': len(self.fallback_docs),
            'embedding_model': self.config.EMBEDDING_MODEL,
            'index_type': 'Fallback Storage'
        }
