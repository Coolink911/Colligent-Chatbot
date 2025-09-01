# 🖥️ Deploy Colligent on VPS/Cloud Server

Deploy on your own server for complete control and custom domain.

## Prerequisites:
- VPS or cloud server (DigitalOcean, AWS, Google Cloud)
- Domain name (optional but recommended)

## Steps:

1. **SSH into your server**:
   ```bash
   ssh user@your-server-ip
   ```

2. **Install dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv nginx
   ```

3. **Clone repository**:
   ```bash
   git clone https://github.com/Coolink911/Colligent-Chatbot.git
   cd Colligent-Chatbot
   ```

4. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Set environment variables**:
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   export OPENAI_MODEL=gpt-3.5-turbo
   ```

6. **Run with systemd service**:
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
   WorkingDirectory=/path/to/Colligent-Chatbot
   Environment="PATH=/path/to/Colligent-Chatbot/venv/bin"
   Environment="OPENAI_API_KEY=your_api_key_here"
   Environment="OPENAI_MODEL=gpt-3.5-turbo"
   ExecStart=/path/to/Colligent-Chatbot/venv/bin/streamlit run colligent_web_app.py --server.port 8501
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

7. **Start the service**:
   ```bash
   sudo systemctl enable colligent
   sudo systemctl start colligent
   ```

8. **Configure Nginx** (for custom domain):
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

9. **Enable the site**:
   ```bash
   sudo ln -s /etc/nginx/sites-available/colligent /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

## Benefits:
- ✅ Complete control
- ✅ Custom domain
- ✅ No usage limits
- ✅ Full customization
- ✅ Professional hosting
