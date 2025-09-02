# 🚀 Colligent Deployment Guide

Your Colligent AI chatbot can be deployed on multiple platforms. Choose the option that works best for you.

## 🌐 **Option 1: Render (Recommended - Easiest)**

**Why Render?**
- ✅ **Completely free** (750 hours/month)
- ✅ **No credit card required**
- ✅ **Fast deployment** (~5-10 minutes)
- ✅ **No timeout issues**

### Deploy Steps:
1. **Go to**: [render.com](https://render.com)
2. **Sign up** with GitHub
3. **Click**: "New +" → "Web Service"
4. **Connect**: `Coolink911/Colligent-Chatbot`
5. **Configure**:
   - **Name**: `colligent-chatbot`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements-ultra-minimal.txt`
   - **Start Command**: `streamlit run colligent_web_app.py --server.port=$PORT --server.address=0.0.0.0`
6. **Add Environment Variables**:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `OPENAI_MODEL`: `gpt-4o-mini`
7. **Click**: "Create Web Service"

**Result**: `https://colligent-chatbot.onrender.com`

---

## 🚂 **Option 2: Railway**

**Why Railway?**
- ✅ **$5 free credit** monthly
- ✅ **Good performance**
- ✅ **Easy deployment**

### Deploy Steps:
1. **Go to**: [railway.app](https://railway.app)
2. **Sign up** with GitHub
3. **Click**: "New Project"
4. **Select**: "Deploy from GitHub repo"
5. **Choose**: `Coolink911/Colligent-Chatbot`
6. **Add Environment Variables** (same as Render)
7. **Wait** for deployment

---

## 🦄 **Option 3: Heroku**

### Deploy Steps:
```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
heroku create your-colligent-app

# Set environment variables
heroku config:set OPENAI_API_KEY=your_key_here
heroku config:set OPENAI_MODEL=gpt-4o-mini

# Deploy
git push heroku main
```

---

## 🐳 **Option 4: Local Docker**

### Deploy Steps:
```bash
# Build image
docker build -f Dockerfile.optimized -t colligent .

# Run container
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=your_key_here \
  -e OPENAI_MODEL=gpt-4o-mini \
  colligent
```

---

## 📱 **Option 5: Streamlit Cloud**

1. **Go to**: [share.streamlit.io](https://share.streamlit.io)
2. **Connect**: Your GitHub repo
3. **Use**: `colligent_web_app.py` as main file
4. **Add environment variables**

---

## 🎯 **Recommended: Render**

**Why Render is best:**
- ✅ **No build timeout issues**
- ✅ **Fast deployment**
- ✅ **Reliable**
- ✅ **Free tier is generous**

**Deploy to Render now**: [render.com](https://render.com)

---

## 🔧 **Environment Variables Required**

All platforms need these environment variables:
```bash
OPENAI_API_KEY=sk-your-openai-key-here
OPENAI_MODEL=gpt-4o-mini
```

---

## 📁 **Repository Structure**

```
collins_personal_agent/
├── colligent_web_app.py          # Main Streamlit app
├── colligent_core.py             # Core chatbot logic
├── colligent_config.py           # Configuration
├── colligent_document_processor.py # Document processing
├── colligent_vector_db.py        # Vector database
├── requirements-ultra-minimal.txt # Dependencies
├── Dockerfile.optimized          # Docker configuration
├── render.yaml                   # Render configuration
├── railway.json                  # Railway configuration
├── .streamlit/                   # Streamlit config
├── data/                         # Your documents
└── README.md                     # Project documentation
```

---

## 🚀 **Quick Start**

1. **Choose platform** (Render recommended)
2. **Connect GitHub repo**
3. **Set environment variables**
4. **Deploy**
5. **Access your app online!**

**Your Colligent app will be live and accessible from anywhere!** 🌐
