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
