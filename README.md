# 🤖 Colligent - Personal AI Assistant

A context-aware chatbot powered by **RAG (Retrieval-Augmented Generation)** that answers questions based on personal documents and research.

## 🚀 Quick Start

### **Local Development**
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
│   └── data/                         # Your documents (CV, research, etc.)
│
├── 🗄️ Database
│   └── vector_db/                    # ChromaDB vector store
│
└── 📋 Configuration Files
    ├── requirements.txt               # Python dependencies
    └── runtime.txt                   # Python version
```

## 🎯 Features

- **🤖 RAG-Powered**: Retrieves relevant information from your documents
- **🎭 Multiple Response Modes**: Professional, storytelling, technical, etc.
- **📄 Multi-Format Support**: PDF and text documents
- **🔒 Fallback System**: Works without external APIs
- **💬 Real-time Chat**: Interactive web interface

## 🌐 Deployment

### **Streamlit Cloud**
1. Push to GitHub
2. Connect to [share.streamlit.io](https://share.streamlit.io)
3. Deploy automatically

### **Local Development**
```bash
# Test the app locally
streamlit run colligent_web_app.py --server.port=8501
```

## 🔧 Configuration

### **Environment Variables**
```bash
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

### **Adding Documents**
1. Place files in `data/` directory
2. Restart the application
3. Use "Rebuild KB" button in web interface

## 🚨 Troubleshooting

### **Common Issues**
- **Dependency conflicts**: Resolved with graceful fallbacks
- **Logger errors**: Fixed in latest version
- **Import issues**: Robust fallback handling implemented

### **Deployment Help**
- **Streamlit Cloud**: Automatic deployment from GitHub
- **Local development**: Test with `streamlit run colligent_web_app.py`



## 🎨 Customization

- **Response modes**: Edit `colligent_core.py`
- **UI changes**: Modify `colligent_web_app.py`
- **RAG parameters**: Adjust `colligent_config.py`
- **Document processing**: Update `colligent_document_processor.py`

## 📄 License

Personal use and educational purposes.

---

**Colligent** | Powered by RAG Technology 🤖✨
