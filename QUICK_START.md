# 🚀 Quick Start: Deploy Colligent in 5 Minutes

## Option 1: Streamlit Cloud (Easiest - Free)

### Step 1: Push to GitHub
```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit"
git branch -M main

# Add your GitHub repository
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file: `colligent_web_app.py`
6. Click "Deploy"

### Step 3: Set Environment Variables
In your Streamlit Cloud app settings, add:
- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_MODEL`: gpt-3.5-turbo

**That's it!** Your app will be live in minutes. 🎉

---

## Option 2: Use the Deployment Script

Run the automated deployment script:
```bash
./deploy.sh
```

This will guide you through all deployment options step-by-step.

---

## What's Been Prepared

✅ **Configuration Updated**: Removed localhost restrictions  
✅ **Requirements Pinned**: Stable dependency versions  
✅ **Security Optimized**: Cloud-ready settings  
✅ **Deployment Files**: Ready for multiple platforms  

---

## Need Help?

- 📖 Read the full [DEPLOYMENT.md](DEPLOYMENT.md) guide
- 🚀 Run `./deploy.sh` for interactive deployment
- 🔧 Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues

Your Colligent app is ready to go live! 🌐
