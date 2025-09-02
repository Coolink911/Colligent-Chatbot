import os
import logging
from typing import List, Dict, Any
import json

from colligent_config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorStore:
    """Fallback vector store implementation for Python 3.13 compatibility"""
    
    def __init__(self, config: Config):
        self.config = config
        self.vector_db = None
        self.collection_name = "documents"
        self.documents = []
        self.metadata = []
        
        # Try to initialize embeddings
        try:
            from langchain_community.embeddings import HuggingFaceEmbeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name=config.EMBEDDING_MODEL,
                model_kwargs={'device': 'cpu'}
            )
            logger.info("Initialized HuggingFace embeddings")
        except Exception as e:
            logger.warning(f"Failed to initialize embeddings: {e}")
            self.embeddings = None
    
    def create_vector_store(self, documents: List[Any]):
        """Create a simple document store (fallback for ChromaDB)"""
        if not documents:
            logger.warning("No documents provided for vector store creation")
            return None
        
        try:
            # Store documents in memory for now
            self.documents = []
            self.metadata = []
            
            for doc in documents:
                if hasattr(doc, 'page_content'):
                    content = doc.page_content
                    meta = getattr(doc, 'metadata', {})
                elif isinstance(doc, dict):
                    content = doc.get('page_content', str(doc))
                    meta = doc.get('metadata', {})
                else:
                    content = str(doc)
                    meta = {}
                
                self.documents.append(content)
                self.metadata.append(meta)
            
            logger.info(f"Created fallback vector store with {len(self.documents)} documents")
            return self
            
        except Exception as e:
            logger.error(f"Error creating fallback vector store: {str(e)}")
            return None
    
    def load_vector_store(self):
        """Load existing vector store (fallback implementation)"""
        try:
            # For now, just return self if we have documents
            if self.documents:
                logger.info("Loaded existing fallback vector store")
                return self
            else:
                logger.info("No existing fallback vector store found")
                return None
        except Exception as e:
            logger.error(f"Error loading fallback vector store: {str(e)}")
            return None
    
    def search_similar(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Simple search implementation (fallback for ChromaDB)"""
        if not self.documents:
            logger.error("Vector store not initialized")
            return []
        
        try:
            # Simple keyword-based search as fallback
            query_lower = query.lower()
            results = []
            
            for i, (doc, meta) in enumerate(zip(self.documents, self.metadata)):
                if query_lower in doc.lower():
                    results.append({
                        'page_content': doc,
                        'metadata': meta,
                        'score': 1.0
                    })
                    if len(results) >= k:
                        break
            
            # If no keyword matches, return first k documents
            if not results:
                for i in range(min(k, len(self.documents))):
                    results.append({
                        'page_content': self.documents[i],
                        'metadata': self.metadata[i] if i < len(self.metadata) else {},
                        'score': 0.5
                    })
            
            logger.info(f"Found {len(results)} similar documents for query: {query[:50]}...")
            return results
            
        except Exception as e:
            logger.error(f"Error searching fallback vector store: {str(e)}")
            return []
    
    def search_with_score(self, query: str, k: int = 5) -> List[tuple]:
        """Search with scores (fallback implementation)"""
        results = self.search_similar(query, k)
        return [(result['page_content'], result['score']) for result in results]
