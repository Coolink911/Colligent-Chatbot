# 🆓 Free Deployment Guide for Colligent

Your Colligent app can be deployed on several free platforms. Here are the best options:

## 🚂 **Option 1: Railway (Recommended)**

### Prerequisites
- GitHub account
- Credit card (for verification only - won't be charged)

### Steps
1. **Go to**: [railway.app](https://railway.app)
2. **Sign up** with GitHub
3. **Click**: "New Project"
4. **Select**: "Deploy from GitHub repo"
5. **Choose**: `Coolink911/Colligent-Chatbot`
6. **Wait** for deployment (5-10 minutes)

### Environment Variables
Add these in Railway dashboard:
- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_MODEL`: `gpt-4o-mini`

### Cost
- **Free**: $5 credit monthly
- **Your app**: Will use ~$1-2/month

---

## 🌐 **Option 2: Render (Completely Free)**

### Prerequisites
- GitHub account
- No credit card required

### Steps
1. **Go to**: [render.com](https://render.com)
2. **Sign up** with GitHub
3. **Click**: "New +" → "Web Service"
4. **Connect**: Your GitHub repo
5. **Configure**:
   - **Name**: `colligent-chatbot`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run colligent_web_app.py --server.port=$PORT --server.address=0.0.0.0`
6. **Add Environment Variables**:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `OPENAI_MODEL`: `gpt-4o-mini`
7. **Click**: "Create Web Service"

### Cost
- **Free**: 750 hours/month
- **Your app**: Will use ~730 hours/month

---

## 🦄 **Option 3: Heroku (Limited Free)**

### Prerequisites
- GitHub account
- Heroku account

### Steps
1. **Install Heroku CLI**
2. **Login**: `heroku login`
3. **Create app**: `heroku create your-colligent-app`
4. **Set environment variables**:
   ```bash
   heroku config:set OPENAI_API_KEY=your_key_here
   heroku config:set OPENAI_MODEL=gpt-4o-mini
   ```
5. **Deploy**: `git push heroku main`

### Cost
- **Free**: Limited dyno hours
- **Your app**: May need paid plan for reliability

---

## 🚀 **Quick Deploy Script**

Run this script to deploy to Railway automatically:

```bash
# Make sure you're in the project directory
cd /path/to/collins_personal_agent

# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Deploy
railway up
```

---

## 🔧 **Troubleshooting**

### Common Issues
1. **Build fails**: Check `requirements.txt` compatibility
2. **App won't start**: Verify environment variables
3. **Search not working**: Check logs for debugging info

### Environment Variables Required
```bash
OPENAI_API_KEY=sk-your-openai-key-here
OPENAI_MODEL=gpt-4o-mini
```

### Check Logs
- **Railway**: Dashboard → Your app → Logs
- **Render**: Dashboard → Your service → Logs
- **Heroku**: `heroku logs --tail`

---

## 🎯 **Recommended: Railway**

**Why Railway?**
- ✅ Most reliable free tier
- ✅ Easy deployment
- ✅ Good performance
- ✅ $5 free credit monthly
- ✅ Your app will cost ~$1-2/month

**Deploy now**: [railway.app](https://railway.app)

---

## 📞 **Need Help?**

1. **Check logs** in your chosen platform
2. **Verify environment variables** are set
3. **Test locally** first: `streamlit run colligent_web_app.py`
4. **Contact support** if deployment fails

Your Colligent app will be live and accessible from anywhere! 🌐
