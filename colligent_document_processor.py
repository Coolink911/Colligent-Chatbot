import os
import logging
from typing import List, Dict, Any
from pathlib import Path

# Add current directory to path for imports
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from colligent_config import Config
    logger = logging.getLogger(__name__)
except ImportError as e:
    print(f"Warning: Could not import colligent_config: {e}")
    logger = None

try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.schema import Document
except ImportError:
    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_core.documents import Document
    except ImportError:
        print("Warning: Could not import text splitters, using fallback")
        RecursiveCharacterTextSplitter = None
        Document = None

import PyPDF2

logging.basicConfig(level=logging.INFO)

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
        
        # Enhanced debugging for cloud deployment
        logger.info(f"Attempting to load documents from: {data_folder}")
        logger.info(f"Current working directory: {os.getcwd()}")
        logger.info(f"Data folder exists: {os.path.exists(data_folder)}")
        logger.info(f"Data folder is directory: {os.path.isdir(data_folder) if os.path.exists(data_folder) else 'N/A'}")
        
        if not os.path.exists(data_folder):
            logger.error(f"Data folder {data_folder} does not exist")
            # Try alternative paths for cloud deployment
            alternative_paths = [
                "data",
                "./data",
                "../data",
                os.path.join(os.getcwd(), "data")
            ]
            
            for alt_path in alternative_paths:
                logger.info(f"Trying alternative path: {alt_path}")
                if os.path.exists(alt_path):
                    logger.info(f"Found data folder at alternative path: {alt_path}")
                    data_folder = alt_path
                    break
            else:
                logger.error("No data folder found in any alternative paths")
                return documents
        
        # List contents of data folder
        try:
            files = os.listdir(data_folder)
            logger.info(f"Files found in data folder: {files}")
        except Exception as e:
            logger.error(f"Error listing data folder contents: {str(e)}")
            return documents
        
        for filename in files:
            file_path = os.path.join(data_folder, filename)
            logger.info(f"Processing file: {filename} at path: {file_path}")
            
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
        
        try:
            chunks = self.text_splitter.split_documents(documents)
            logger.info(f"Split {len(documents)} documents into {len(chunks)} chunks")
            return chunks
        except Exception as e:
            logger.error(f"Error splitting documents: {str(e)}")
            return []
    
    def process_documents(self) -> List[Document]:
        """Complete document processing pipeline"""
        try:
            documents = self.load_documents()
            if not documents:
                logger.error("No documents loaded - cannot create knowledge base")
                return []
            
            chunks = self.split_documents(documents)
            if not chunks:
                logger.error("No chunks created from documents")
                return []
            
            logger.info(f"Document processing complete: {len(documents)} documents -> {len(chunks)} chunks")
            return chunks
            
        except Exception as e:
            logger.error(f"Error in document processing pipeline: {str(e)}")
            return []
