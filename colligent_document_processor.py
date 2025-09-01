import os
import PyPDF2
from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter
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

class DocumentProcessor:
    """Handles document loading, text extraction, and chunking"""
    
    def __init__(self, config: Config):
        self.config = config
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            length_function=len,
        )
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from a PDF file"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {str(e)}")
            return ""
    
    def load_documents(self) -> List[Document]:
        """Load all documents from the data folder"""
        documents = []
        data_folder = self.config.DATA_FOLDER
        
        logger.info(f"Looking for data folder at: {data_folder}")
        logger.info(f"Current working directory: {os.getcwd()}")
        logger.info(f"Files in current directory: {os.listdir('.')}")
        
        if not os.path.exists(data_folder):
            logger.error(f"Data folder {data_folder} does not exist")
            # Try alternative paths
            alt_paths = [
                "data",
                "../data",
                "./data",
                os.path.join(os.getcwd(), "data")
            ]
            for alt_path in alt_paths:
                if os.path.exists(alt_path):
                    logger.info(f"Found data folder at alternative path: {alt_path}")
                    data_folder = alt_path
                    break
            else:
                logger.error("Could not find data folder in any location")
                return documents
        
        logger.info(f"Using data folder: {data_folder}")
        logger.info(f"Files in data folder: {os.listdir(data_folder) if os.path.exists(data_folder) else 'NOT FOUND'}")
        
        for filename in os.listdir(data_folder):
            file_path = os.path.join(data_folder, filename)
            logger.info(f"Processing file: {filename} at {file_path}")
            
            if filename.lower().endswith('.pdf'):
                logger.info(f"Processing PDF: {filename}")
                text = self.extract_text_from_pdf(file_path)
                if text.strip():
                    doc = Document(
                        page_content=text,
                        metadata={"source": filename, "type": "pdf"}
                    )
                    documents.append(doc)
                    logger.info(f"Successfully processed PDF: {filename} ({len(text)} characters)")
                else:
                    logger.warning(f"PDF {filename} produced empty text")
            
            elif filename.lower().endswith('.txt'):
                logger.info(f"Processing text file: {filename}")
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        text = file.read()
                        doc = Document(
                            page_content=text,
                            metadata={"source": filename, "type": "text"}
                        )
                        documents.append(doc)
                        logger.info(f"Successfully processed text file: {filename} ({len(text)} characters)")
                except Exception as e:
                    logger.error(f"Error reading text file {file_path}: {str(e)}")
        
        logger.info(f"Loaded {len(documents)} documents")
        return documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks"""
        if not documents:
            return []
        
        chunks = self.text_splitter.split_documents(documents)
        logger.info(f"Split {len(documents)} documents into {len(chunks)} chunks")
        return chunks
    
    def process_documents(self) -> List[Dict[str, Any]]:
        """Complete document processing pipeline"""
        documents = self.load_documents()
        chunks = self.split_documents(documents)
        
        # Convert to format expected by vector database
        processed_chunks = []
        for chunk in chunks:
            processed_chunks.append({
                'content': chunk.page_content,
                'metadata': chunk.metadata
            })
        
        return processed_chunks
