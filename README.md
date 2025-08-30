# 🤖 Collins' Personal AI Assistant

A context-aware chatbot powered by **RAG (Retrieval-Augmented Generation)** that answers questions based on personal documents and research. Collins' Personal AI Assistant provides intelligent responses grounded in specific content through advanced natural language processing and vector search.

## 🚀 Quick Start

### **Streamlit Web Interface**
```bash
# Install dependencies
pip install -r requirements.txt

# Run the web app
streamlit run colligent_web_app.py
```
Access at: `http://localhost:8501`

## 📁 Project Structure

```
collins_personal_agent/
├── 📄 Core Application
│   ├── colligent_web_app.py          # Main Streamlit interface
│   ├── colligent_core.py             # Core chatbot logic
│   ├── colligent_config.py           # Configuration settings
│   ├── colligent_vector_db.py        # Vector database operations
│   └── colligent_document_processor.py # Document processing
│
├── 📚 Knowledge Base
│   └── data/
│       ├── Collins_cv_2025-1-2.pdf   # CV document
│       ├── Collins_cv_2025-1-2.txt   # CV text version
│       ├── Draft msc.pdf             # Research document
│       ├── Draft msc.txt             # Research text version
│       ├── best_model.py             # Diffusion model code
│       └── best_model.txt            # Model documentation
│
├── 📋 Configuration
│   ├── README.md                     # Project documentation
│   ├── requirements.txt              # Python dependencies
│   ├── Dockerfile                    # Container deployment
│   ├── Procfile                      # Heroku deployment
│   └── runtime.txt                   # Python version
│
└── 🗄️ Database
    └── vector_db/                    # ChromaDB vector store
```

## 🎯 Features

### **🤖 Intelligent Responses**
- **RAG-Powered**: Retrieves relevant information from documents
- **Context-Aware**: Answers based on actual content, not generic knowledge
- **Multi-Modal**: Supports PDF and text documents
- **Fallback System**: Works without external APIs

### **🎭 Response Modes**
- **💬 Default**: Natural conversational tone
- **👔 Interview**: Professional & concise
- **📖 Storytelling**: Narrative & reflective
- **⚡ Fast Facts**: Bullet points & TL;DR
- **💪 Humble Brag**: Confident self-promotion
- **💻 Code Style**: Technical & implementation-focused

### **🔧 Interactive Features**
- **Real-time Chat**: Immediate responses with source attribution
- **Context Display**: See which documents were used
- **Mode Switching**: Change response style on the fly
- **Knowledge Base Management**: Rebuild and update documents

## 🧠 "Show Your Thinking" Artifacts

### **1. Agent Instructions & System Prompts**

#### **Core Agent Instructions**
```python
# From colligent_config.py
SYSTEM_PROMPT = """
You are Collins, a Data Scientist and Astrophysics Researcher. You have access to Collins' personal documents including CV, research papers, and technical implementations.

Your role is to:
- Answer questions based on Collins' actual documents and experiences
- Use "I" and "my" to refer to Collins' experiences, skills, and background
- Reference the documents as "my CV", "my research", "my work", etc.
- Be personal and authentic to Collins' voice and style
- Base all answers on the information in Collins' documents
- If the context doesn't contain enough information to answer the question, respond with: "I do not have available information yet."
- Be concise but thorough in your responses
- Maintain Collins' professional yet approachable tone
"""
```

#### **Response Mode Transformations**
```python
# From colligent_core.py - Response Mode System
def _transform_to_code_style_mode(self, response: str) -> str:
    """Transform response to technical implementation-focused mode"""
    if "I am" in response:
        response = response.replace("I am", "From a technical implementation perspective, I am")
    if "diffusion models" in response.lower():
        response += " In my implementation, I use a ContextU-Net architecture with residual connections, designed for conditional image generation using diffusion processes."
    if "machine learning" in response.lower():
        response += " My approach involves implementing residual convolutional blocks with batch normalization and ReLU activation."
    return response
```

### **2. Sub-Agent Roles & Responsibilities**

#### **Document Processing Agent**
```python
# From colligent_document_processor.py
class DocumentProcessor:
    """Sub-agent responsible for document ingestion and processing"""
    
    def process_documents(self) -> List[Document]:
        """Main processing pipeline"""
        # 1. Load documents from data directory
        # 2. Extract text from PDFs and text files
        # 3. Clean and preprocess text
        # 4. Split into chunks with overlap
        # 5. Add metadata for source tracking
```

#### **Vector Database Agent**
```python
# From colligent_vector_db.py
class VectorStore:
    """Sub-agent responsible for semantic search and retrieval"""
    
    def search_similar(self, query: str, k: int = 5) -> List[Document]:
        """Semantic similarity search"""
        # 1. Convert query to embedding
        # 2. Search vector database
        # 3. Return top-k most similar documents
        # 4. Include similarity scores
```

#### **Response Generation Agent**
```python
# From colligent_core.py
class ContextAwareChatbot:
    """Main orchestration agent with multiple sub-agents"""
    
    def ask_question(self, query: str, include_context: bool = False) -> Dict[str, Any]:
        """Main question-answering pipeline"""
        # 1. Get relevant context from VectorStore agent
        # 2. Apply response mode transformation
        # 3. Generate response using LLM or fallback
        # 4. Return response with sources
```

### **3. Prompt Engineering & Decision Trees**

#### **Context Assembly Prompt**
```python
def create_prompt(self, query: str, context: str) -> str:
    """Create a prompt for the LLM with context and query"""
    prompt_template = f"""
{self.config.SYSTEM_PROMPT}

Context from documents:
{context}

User Question: {query}

Please answer the question based on the provided context. If the context doesn't contain enough information to answer the question, respond with: "I do not have available information yet."
"""
    return prompt_template
```

#### **Response Strategy Decision Tree**
```python
def choose_response_strategy(self, query: str, context: str, llm_available: bool) -> str:
    """Decision tree for response generation strategy"""
    
    # Decision 1: LLM Availability
    if llm_available:
        strategy = "openai_gpt"
    else:
        strategy = "pattern_based"
    
    # Decision 2: Context Quality
    if not context or context == "No relevant information found in the documents.":
        return "I do not have available information yet."
    
    # Decision 3: Response Mode Application
    if self.current_mode != "default":
        return self.apply_mode_transformation(response, self.current_mode)
    
    return response
```

### **4. RAG Pipeline Visualization**

#### **Complete RAG Process**
```python
def visualize_rag_process(self, query: str) -> Dict[str, Any]:
    """Shows the complete RAG process for a given query"""
    
    # Step 1: Query Processing
    query_embedding = self.vector_store.embeddings.encode(query)
    
    # Step 2: Retrieval
    similar_chunks = self.vector_store.search_similar(query, k=5)
    
    # Step 3: Context Assembly
    context = self.assemble_context(similar_chunks)
    
    # Step 4: Response Generation
    response = self.generate_response(query, context)
    
    return {
        'query': query,
        'query_embedding_shape': query_embedding.shape,
        'retrieved_chunks': len(similar_chunks),
        'context_length': len(context),
        'response_length': len(response),
        'sources': self.extract_sources(similar_chunks)
    }
```

### **5. Error Handling & Fallback Systems**

#### **Graceful Degradation**
```python
def get_fallback_response(self, query: str, context: str) -> str:
    """Fallback system when LLM is unavailable"""
    
    # Check if context is insufficient
    if not self._context_contains_relevant_info(context, query):
        return "I do not have available information yet."
    
    # Pattern-based response generation
    query_lower = query.lower()
    
    if any(word in query_lower for word in ['skill', 'technology', 'programming']):
        return self._extract_technical_skills(context, query)
    elif any(word in query_lower for word in ['experience', 'work', 'job']):
        return self._extract_experience_info(context, query)
    elif any(word in query_lower for word in ['research', 'study', 'project']):
        return self._extract_research_info(context, query)
    else:
        return self._extract_general_info(context, query)
```

## 💡 Sample Questions & Responses

### **Professional Background**
**Q: "What kind of engineer am I?"**
```
Expected Answer: "I'm a Data Scientist and Astrophysics Researcher. I work at the intersection of machine learning and cosmology, specializing in predicting universe seeing conditions, emulating cosmic structures with AI, and solving theoretical puzzles in astrophysics."

RAG Process:
1. Retrieval: Finds chunks about role, specialization, and background
2. Generation: Combines information into coherent professional description
3. Sources: Collins_cv_2025-1-2.pdf, Draft msc.pdf
```

### **Technical Expertise**
**Q: "Explain my diffusion model research"**
```
Expected Answer: "My diffusion model research focuses on emulating neutral hydrogen maps using a ContextU-Net architecture. I implement residual convolutional blocks with batch normalization and ReLU activation, supporting both residual and non-residual modes with dynamic channel adjustment."

RAG Process:
1. Retrieval: Identifies technical implementation details from best_model.txt
2. Generation: Synthesizes technical approach with implementation specifics
3. Sources: best_model.txt, best_model.py
```

## 🛠️ Technical Architecture

### **Core Components**
1. **Document Processor**: Extracts and chunks text from PDFs and documents
2. **Vector Store**: ChromaDB with sentence transformers for semantic search
3. **Chatbot Engine**: OpenAI GPT + fallback system for response generation
4. **Web Interfaces**: Streamlit and Flask for different use cases

### **RAG Pipeline**
1. **📄 Document Loading**: PDF extraction and text processing
2. **✂️ Chunking**: 1000-character chunks with 200-character overlap
3. **🔍 Embedding**: Semantic vectorization using all-MiniLM-L6-v2
4. **🎯 Retrieval**: Top-5 most similar chunks for context
5. **🤖 Generation**: Context-aware response with source attribution

## 🔧 Configuration

### **Environment Variables**
```bash
# Copy env_example.txt to .env and fill in your values
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
```

### **Security Features**
- **Input Validation**: Prevents XSS and injection attacks
- **Rate Limiting**: 30 requests per minute per user
- **Output Sanitization**: Removes potentially harmful content
- **Session Management**: Secure session handling
- **CORS Protection**: Disabled for local deployment
- **XSRF Protection**: Enabled for form security

### **Customization**
- Add documents to `data/` folder
- Modify response modes in `colligent_core.py`
- Customize UI in `colligent_web_app.py`
- Adjust RAG parameters in `colligent_config.py`

## 📊 Knowledge Base

### **Current Documents**
- **CV & Background**: Professional experience and skills
- **Research Papers**: Academic work and publications
- **Code Documentation**: Technical implementations and approaches

### **Adding New Documents**
1. Place files in `data/` directory
2. Restart the application
3. Use "Rebuild KB" button in web interface

## 🎨 Customization

- **Add Documents**: Place files in `data/` directory
- **Modify Response Modes**: Edit `colligent_core.py`
- **Customize UI**: Edit `colligent_web_app.py`
- **Adjust RAG Parameters**: Edit `colligent_config.py`

## 🚀 Deployment

### **Streamlit Cloud (Recommended)**
1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Deploy automatically

### **Heroku**
1. Add `Procfile` and `runtime.txt`
2. Configure buildpacks
3. Deploy via Heroku CLI

### **Docker**
```bash
docker build -t colligent .
docker run -p 8501:8501 colligent
```

## 📄 License

This project is for personal use and educational purposes.

---

**Collins' Personal AI Assistant** | Powered by RAG Technology 🤖✨
