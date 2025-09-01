import os
import logging
from typing import List, Dict, Any, Optional
import numpy as np

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

# Try to import FAISS
try:
    import faiss
    FAISS_AVAILABLE = True
    logger.info("FAISS imported successfully")
except ImportError as e:
    logger.error(f"FAISS import failed: {e}")
    FAISS_AVAILABLE = False

from sentence_transformers import SentenceTransformer

class VectorStore:
    """Vector store for document embeddings using FAISS only"""
    
    def __init__(self, config: Config):
        self.config = config
        self.vector_db_path = config.VECTOR_DB_PATH
        self.embedding_model = SentenceTransformer(config.EMBEDDING_MODEL)
        self.chunk_size = config.CHUNK_SIZE
        self.chunk_overlap = config.CHUNK_OVERLAP
        
        # Initialize FAISS storage
        self.faiss_index = None
        self.documents = []
        self.metadata = []
    
    def create_vector_store(self, documents: List[Dict[str, Any]]) -> bool:
        """Create vector store from documents"""
        if not FAISS_AVAILABLE:
            logger.error("FAISS not available")
            return False
            
        try:
            return self._create_faiss_store(documents)
        except Exception as e:
            logger.error(f"Error creating vector store: {e}")
            return False
    
    def _create_faiss_store(self, documents: List[Dict[str, Any]]) -> bool:
        """Create FAISS vector store"""
        try:
            # Extract text content
            texts = [doc['content'] for doc in documents]
            self.metadata = [doc['metadata'] for doc in documents]
            
            # Create embeddings
            embeddings = self.embedding_model.encode(texts)
            
            # Create FAISS index
            dimension = embeddings.shape[1]
            self.faiss_index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
            
            # Normalize embeddings for cosine similarity
            faiss.normalize_L2(embeddings)
            
            # Add to index
            self.faiss_index.add(embeddings.astype('float32'))
            self.documents = texts
            
            # Save the store
            self.save_faiss_store()
            
            logger.info(f"Created FAISS index with {len(documents)} documents")
            return True
            
        except Exception as e:
            logger.error(f"FAISS creation failed: {e}")
            return False
    
    def load_vector_store(self) -> bool:
        """Load existing vector store"""
        if not FAISS_AVAILABLE:
            return False
            
        try:
            return self._load_faiss_store()
        except Exception as e:
            logger.error(f"Error loading vector store: {e}")
            return False
    
    def _load_faiss_store(self) -> bool:
        """Load existing FAISS store"""
        try:
            index_path = os.path.join(self.vector_db_path, "faiss_index.bin")
            docs_path = os.path.join(self.vector_db_path, "documents.txt")
            meta_path = os.path.join(self.vector_db_path, "metadata.txt")
            
            if not all(os.path.exists(p) for p in [index_path, docs_path, meta_path]):
                return False
            
            # Load FAISS index
            self.faiss_index = faiss.read_index(index_path)
            
            # Load documents and metadata
            with open(docs_path, 'r', encoding='utf-8') as f:
                self.documents = [line.strip() for line in f.readlines()]
            
            with open(meta_path, 'r', encoding='utf-8') as f:
                self.metadata = [eval(line.strip()) for line in f.readlines()]
            
            logger.info("FAISS store loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load FAISS store: {e}")
            return False
    
    def search_similar(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        if not FAISS_AVAILABLE or self.faiss_index is None:
            logger.warning("FAISS not available for search")
            return []
            
        try:
            return self._search_faiss(query, k)
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []
    
    def _search_faiss(self, query: str, k: int) -> List[Dict[str, Any]]:
        """Search using FAISS"""
        try:
            # Create query embedding
            query_embedding = self.embedding_model.encode([query])
            faiss.normalize_L2(query_embedding)
            
            # Search
            scores, indices = self.faiss_index.search(
                query_embedding.astype('float32'), k
            )
            
            # Return results
            documents = []
            for idx, score in zip(indices[0], scores[0]):
                if idx < len(self.documents):
                    doc = {
                        'page_content': self.documents[idx],
                        'metadata': self.metadata[idx] if idx < len(self.metadata) else {},
                        'score': float(score)
                    }
                    documents.append(doc)
            
            return documents
            
        except Exception as e:
            logger.error(f"FAISS search failed: {e}")
            return []
    
    def save_faiss_store(self):
        """Save FAISS store to disk"""
        if not FAISS_AVAILABLE or self.faiss_index is None:
            return
        
        try:
            os.makedirs(self.vector_db_path, exist_ok=True)
            
            # Save FAISS index
            index_path = os.path.join(self.vector_db_path, "faiss_index.bin")
            faiss.write_index(self.faiss_index, index_path)
            
            # Save documents
            docs_path = os.path.join(self.vector_db_path, "documents.txt")
            with open(docs_path, 'w', encoding='utf-8') as f:
                for doc in self.documents:
                    f.write(doc + '\n')
            
            # Save metadata
            meta_path = os.path.join(self.vector_db_path, "metadata.txt")
            with open(meta_path, 'w', encoding='utf-8') as f:
                for meta in self.metadata:
                    f.write(str(meta) + '\n')
            
            logger.info("FAISS store saved successfully")
            
        except Exception as e:
            logger.error(f"Failed to save FAISS store: {e}")
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the vector store"""
        if not FAISS_AVAILABLE or self.faiss_index is None:
            return {"error": "Vector store not initialized"}
        
        try:
            return {
                "collection_name": "faiss_documents",
                "document_count": len(self.documents),
                "embedding_model": self.config.EMBEDDING_MODEL,
                "index_type": "FAISS"
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {"error": str(e)}
