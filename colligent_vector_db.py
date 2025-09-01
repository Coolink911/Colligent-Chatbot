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

# Global flags for optional imports
CHROMADB_AVAILABLE = False
FAISS_AVAILABLE = False

# Try to import optional dependencies
def _check_imports():
    global CHROMADB_AVAILABLE, FAISS_AVAILABLE
    
    try:
        import chromadb
        from chromadb.config import Settings
        CHROMADB_AVAILABLE = True
        logger.info("ChromaDB imported successfully")
    except ImportError as e:
        logger.warning(f"ChromaDB import failed: {e}. Will use FAISS fallback.")
        CHROMADB_AVAILABLE = False
    except RuntimeError as e:
        logger.warning(f"ChromaDB runtime error: {e}. Will use FAISS fallback.")
        CHROMADB_AVAILABLE = False

    try:
        import faiss
        FAISS_AVAILABLE = True
        logger.info("FAISS imported successfully")
    except ImportError as e:
        logger.error(f"FAISS import failed: {e}")
        FAISS_AVAILABLE = False

# Check imports when module is loaded
_check_imports()

from sentence_transformers import SentenceTransformer

class VectorStore:
    """Vector store for document embeddings with fallback support"""
    
    def __init__(self, config: Config):
        self.config = config
        self.vector_db_path = config.VECTOR_DB_PATH
        self.embedding_model = SentenceTransformer(config.EMBEDDING_MODEL)
        self.chunk_size = config.CHUNK_SIZE
        self.chunk_overlap = config.CHUNK_OVERLAP
        
        # Initialize storage
        self.chroma_client = None
        self.collection = None
        self.faiss_index = None
        self.documents = []
        self.metadata = []
    
    def create_vector_store(self, documents: List[Dict[str, Any]]) -> bool:
        """Create vector store from documents"""
        try:
            if CHROMADB_AVAILABLE:
                return self._create_chromadb_store(documents)
            elif FAISS_AVAILABLE:
                return self._create_faiss_store(documents)
            else:
                logger.error("No vector database backend available")
                return False
        except Exception as e:
            logger.error(f"Error creating vector store: {e}")
            return False
    
    def _create_chromadb_store(self, documents: List[Dict[str, Any]]) -> bool:
        """Create ChromaDB vector store"""
        try:
            # Import chromadb here to avoid module-level import issues
            import chromadb
            from chromadb.config import Settings
            
            # Create ChromaDB client
            self.chroma_client = chromadb.PersistentClient(
                path=self.vector_db_path,
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Create or get collection
            collection_name = "colligent_documents"
            try:
                self.collection = self.chroma_client.get_collection(collection_name)
                logger.info("Using existing ChromaDB collection")
            except:
                self.collection = self.chroma_client.create_collection(
                    name=collection_name,
                    metadata={"hnsw:space": "cosine"}
                )
                logger.info("Created new ChromaDB collection")
            
            # Add documents
            texts = [doc['content'] for doc in documents]
            metadatas = [doc['metadata'] for doc in documents]
            ids = [f"doc_{i}" for i in range(len(documents))]
            
            self.collection.add(
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Added {len(documents)} documents to ChromaDB")
            return True
            
        except Exception as e:
            logger.error(f"ChromaDB creation failed: {e}")
            return False
    
    def _create_faiss_store(self, documents: List[Dict[str, Any]]) -> bool:
        """Create FAISS vector store as fallback"""
        try:
            # Import faiss here to avoid module-level import issues
            import faiss
            
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
            
            logger.info(f"Created FAISS index with {len(documents)} documents")
            return True
            
        except Exception as e:
            logger.error(f"FAISS creation failed: {e}")
            return False
    
    def load_vector_store(self) -> bool:
        """Load existing vector store"""
        try:
            if CHROMADB_AVAILABLE:
                return self._load_chromadb_store()
            elif FAISS_AVAILABLE:
                return self._load_faiss_store()
            else:
                return False
        except Exception as e:
            logger.error(f"Error loading vector store: {e}")
            return False
    
    def _load_chromadb_store(self) -> bool:
        """Load existing ChromaDB store"""
        try:
            if not os.path.exists(self.vector_db_path):
                return False
            
            # Import chromadb here
            import chromadb
            from chromadb.config import Settings
            
            self.chroma_client = chromadb.PersistentClient(
                path=self.vector_db_path,
                settings=Settings(anonymized_telemetry=False)
            )
            
            collection_name = "colligent_documents"
            self.collection = self.chroma_client.get_collection(collection_name)
            
            logger.info("ChromaDB store loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load ChromaDB store: {e}")
            return False
    
    def _load_faiss_store(self) -> bool:
        """Load existing FAISS store"""
        try:
            # Import faiss here
            import faiss
            
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
        try:
            logger.info(f"Starting search for: {query}")
            logger.info(f"CHROMADB_AVAILABLE: {CHROMADB_AVAILABLE}, collection: {self.collection is not None}")
            logger.info(f"FAISS_AVAILABLE: {FAISS_AVAILABLE}, faiss_index: {self.faiss_index is not None}")
            
            if CHROMADB_AVAILABLE and self.collection:
                logger.info("Using ChromaDB for search")
                return self._search_chromadb(query, k)
            elif FAISS_AVAILABLE and self.faiss_index is not None:
                logger.info("Using FAISS for search")
                return self._search_faiss(query, k)
            else:
                logger.warning("No vector store available for search")
                return []
        except Exception as e:
            logger.error(f"Search error: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return []
    
    def _search_chromadb(self, query: str, k: int) -> List[Dict[str, Any]]:
        """Search using ChromaDB"""
        try:
            logger.info(f"Searching ChromaDB for: {query}")
            results = self.collection.query(
                query_texts=[query],
                n_results=k
            )
            
            logger.info(f"ChromaDB results keys: {results.keys()}")
            logger.info(f"Documents found: {len(results['documents'][0]) if results['documents'] else 0}")
            
            documents = []
            for i in range(len(results['documents'][0])):
                doc = {
                    'page_content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {}
                }
                documents.append(doc)
                logger.info(f"Document {i}: content length={len(doc['page_content'])}, metadata={doc['metadata']}")
            
            logger.info(f"Returning {len(documents)} documents from ChromaDB search")
            return documents
            
        except Exception as e:
            logger.error(f"ChromaDB search failed: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return []
    
    def _search_faiss(self, query: str, k: int) -> List[Dict[str, Any]]:
        """Search using FAISS"""
        try:
            logger.info(f"Searching FAISS for: {query}")
            # Import faiss here
            import faiss
            
            # Create query embedding
            query_embedding = self.embedding_model.encode([query])
            faiss.normalize_L2(query_embedding)
            
            # Search
            scores, indices = self.faiss_index.search(
                query_embedding.astype('float32'), k
            )
            
            logger.info(f"FAISS search returned {len(indices[0])} results")
            
            # Return results
            documents = []
            for i, (idx, score) in enumerate(zip(indices[0], scores[0])):
                if idx < len(self.documents):
                    doc = {
                        'page_content': self.documents[idx],
                        'metadata': self.metadata[idx] if idx < len(self.metadata) else {},
                        'score': float(score)
                    }
                    documents.append(doc)
                    logger.info(f"FAISS Document {i}: content length={len(doc['page_content'])}, metadata={doc['metadata']}")
                else:
                    logger.warning(f"FAISS index {idx} out of range (max: {len(self.documents)})")
            
            logger.info(f"Returning {len(documents)} documents from FAISS search")
            return documents
            
        except Exception as e:
            logger.error(f"FAISS search failed: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return []
    
    def save_faiss_store(self):
        """Save FAISS store to disk"""
        if not FAISS_AVAILABLE or self.faiss_index is None:
            return
        
        try:
            # Import faiss here
            import faiss
            
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
        try:
            if CHROMADB_AVAILABLE and self.collection:
                # Get ChromaDB collection info
                count = self.collection.count()
                return {
                    "collection_name": "colligent_documents",
                    "document_count": count,
                    "embedding_model": self.config.EMBEDDING_MODEL,
                    "index_type": "ChromaDB"
                }
            elif FAISS_AVAILABLE and self.faiss_index is not None:
                # Get FAISS collection info
                return {
                    "collection_name": "faiss_documents",
                    "document_count": len(self.documents),
                    "embedding_model": self.config.EMBEDDING_MODEL,
                    "index_type": "FAISS"
                }
            else:
                return {"error": "Vector store not initialized"}
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {"error": str(e)}
