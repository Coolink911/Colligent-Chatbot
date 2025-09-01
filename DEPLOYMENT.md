# 🚀 Colligent Deployment Guide

This guide will help you deploy your Colligent application online for easier access.

## Option 1: Streamlit Cloud (Recommended - Free & Easy)

### Prerequisites
1. GitHub account
2. Your code pushed to a GitHub repository

### Steps:
1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set the main file path to: `colligent_web_app.py`
   - Click "Deploy"

3. **Set Environment Variables:**
   - In your Streamlit Cloud app settings, add:
     - `OPENAI_API_KEY`: Your OpenAI API key
     - `OPENAI_MODEL`: gpt-3.5-turbo (or your preferred model)

### Benefits:
- ✅ Free hosting
- ✅ Automatic HTTPS
- ✅ Easy deployment
- ✅ Built-in analytics
- ✅ Automatic updates from GitHub

---

## Option 2: Railway (Alternative - Free Tier)

### Steps:
1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Create new project
4. Connect your GitHub repository
5. Set environment variables
6. Deploy

---

## Option 3: Heroku (Paid - More Control)

### Prerequisites:
1. Heroku account
2. Heroku CLI installed

### Steps:
1. **Install Heroku CLI:**
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login to Heroku:**
   ```bash
   heroku login
   ```

3. **Create Heroku app:**
   ```bash
   heroku create your-colligent-app
   ```

4. **Set environment variables:**
   ```bash
   heroku config:set OPENAI_API_KEY=your_api_key_here
   heroku config:set OPENAI_MODEL=gpt-3.5-turbo
   ```

5. **Deploy:**
   ```bash
   git push heroku main
   ```

---

## Option 4: VPS/Cloud Server (Advanced - Full Control)

### Prerequisites:
1. VPS or cloud server (DigitalOcean, AWS, Google Cloud)
2. Domain name (optional)

### Steps:
1. **SSH into your server:**
   ```bash
   ssh user@your-server-ip
   ```

2. **Install dependencies:**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip nginx
   ```

3. **Clone your repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
   ```

4. **Install Python dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

5. **Run with systemd service:**
   ```bash
   sudo nano /etc/systemd/system/colligent.service
   ```

   Add this content:
   ```ini
   [Unit]
   Description=Colligent Streamlit App
   After=network.target

   [Service]
   User=your-username
   WorkingDirectory=/path/to/your/app
   Environment="PATH=/path/to/your/app/venv/bin"
   ExecStart=/path/to/your/app/venv/bin/streamlit run colligent_web_app.py --server.port 8501
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

6. **Start the service:**
   ```bash
   sudo systemctl enable colligent
   sudo systemctl start colligent
   ```

7. **Configure Nginx (optional):**
   ```bash
   sudo nano /etc/nginx/sites-available/colligent
   ```

   Add this content:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

8. **Enable the site:**
   ```bash
   sudo ln -s /etc/nginx/sites-available/colligent /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

---

## Environment Variables

Make sure to set these in your deployment platform:

```bash
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
```

---

## Security Considerations

1. **API Keys:** Never commit API keys to your repository
2. **Rate Limiting:** Your app includes built-in rate limiting
3. **Input Validation:** Built-in XSS protection
4. **HTTPS:** Use HTTPS in production

---

## Troubleshooting

### Common Issues:

1. **Import Errors:** Make sure all dependencies are in `requirements.txt`
2. **Port Issues:** Streamlit runs on port 8501 by default
3. **Memory Issues:** Consider using lighter models for free tiers
4. **Vector DB:** The app will recreate the vector database on first run

### Getting Help:

- Check Streamlit Cloud logs
- Verify environment variables are set
- Ensure all files are committed to GitHub
- Check the app runs locally first

---

## Next Steps

After deployment:
1. Test your app thoroughly
2. Set up monitoring (if using paid platforms)
3. Configure custom domain (optional)
4. Set up CI/CD for automatic deployments

Your Colligent app should now be accessible online! 🎉
