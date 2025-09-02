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
    ├── requirements-render-flexible.txt # Render deployment
    ├── render-main-app.yaml          # Render configuration
    └── runtime.txt                   # Python version
```

## 🎯 Features

- **🤖 RAG-Powered**: Retrieves relevant information from your documents
- **🎭 Multiple Response Modes**: Professional, storytelling, technical, etc.
- **📄 Multi-Format Support**: PDF and text documents
- **🔒 Fallback System**: Works without external APIs
- **💬 Real-time Chat**: Interactive web interface

## 🌐 Deployment

### **Render (Recommended - Free)**
1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect your GitHub repo: `Coolink911/Colligent-Chatbot`
4. Use configuration from `render-main-app.yaml`
5. Set environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `OPENAI_MODEL`: `gpt-4o-mini`

### **Streamlit Cloud**
1. Push to GitHub
2. Connect to [share.streamlit.io](https://share.streamlit.io)
3. Deploy automatically

### **Local Development**
```bash
# Test the app locally
streamlit run colligent_web_app.py --server.port=8501

# Test simple version
streamlit run simple_test_app.py --server.port=8502
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
- **Dependency conflicts**: Use `requirements-render-flexible.txt`
- **Logger errors**: Fixed in latest version
- **Import issues**: Robust fallback handling implemented

### **Deployment Help**
- **Simple test app**: `simple_test_app.py` for debugging
- **Multiple configs**: Different requirements files for different platforms
- **Detailed guides**: Check `RENDER_DEPLOY_FIXED.md`



## 🎨 Customization

- **Response modes**: Edit `colligent_core.py`
- **UI changes**: Modify `colligent_web_app.py`
- **RAG parameters**: Adjust `colligent_config.py`
- **Document processing**: Update `colligent_document_processor.py`

## 📄 License

Personal use and educational purposes.

---

**Colligent** | Powered by RAG Technology 🤖✨
