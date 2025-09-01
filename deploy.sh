#!/bin/bash

# 🚀 Colligent Deployment Script
# This script helps deploy your Colligent app to various platforms

echo "🚀 Welcome to Colligent Deployment!"
echo "=================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit"
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Function to deploy to Streamlit Cloud
deploy_streamlit() {
    echo "🌐 Deploying to Streamlit Cloud..."
    echo ""
    echo "📋 Steps to complete:"
    echo "1. Go to https://share.streamlit.io"
    echo "2. Sign in with GitHub"
    echo "3. Click 'New app'"
    echo "4. Select this repository"
    echo "5. Set main file path to: colligent_web_app.py"
    echo "6. Click 'Deploy'"
    echo ""
    echo "🔑 Don't forget to set environment variables:"
    echo "   - OPENAI_API_KEY"
    echo "   - OPENAI_MODEL"
    echo ""
    read -p "Press Enter when you're ready to continue..."
}

# Function to deploy to Railway
deploy_railway() {
    echo "🚂 Deploying to Railway..."
    echo ""
    echo "📋 Steps to complete:"
    echo "1. Go to https://railway.app"
    echo "2. Sign in with GitHub"
    echo "3. Create new project"
    echo "4. Connect this repository"
    echo "5. Set environment variables"
    echo "6. Deploy"
    echo ""
    read -p "Press Enter when you're ready to continue..."
}

# Function to deploy to Heroku
deploy_heroku() {
    echo "🦄 Deploying to Heroku..."
    
    # Check if Heroku CLI is installed
    if ! command -v heroku &> /dev/null; then
        echo "❌ Heroku CLI not found. Installing..."
        curl https://cli-assets.heroku.com/install.sh | sh
    fi
    
    echo "🔐 Logging into Heroku..."
    heroku login
    
    echo "🏗️ Creating Heroku app..."
    read -p "Enter your app name (or press Enter for auto-generated): " app_name
    
    if [ -z "$app_name" ]; then
        heroku create
    else
        heroku create "$app_name"
    fi
    
    echo "🔑 Setting environment variables..."
    read -p "Enter your OpenAI API key: " api_key
    heroku config:set OPENAI_API_KEY="$api_key"
    heroku config:set OPENAI_MODEL="gpt-3.5-turbo"
    
    echo "🚀 Deploying to Heroku..."
    git push heroku main
    
    echo "✅ Deployment complete!"
    heroku open
}

# Function to prepare for VPS deployment
deploy_vps() {
    echo "🖥️ Preparing for VPS deployment..."
    echo ""
    echo "📋 Files created for VPS deployment:"
    echo "✅ colligent.service (systemd service file)"
    echo "✅ nginx.conf (Nginx configuration)"
    echo "✅ deploy_vps.sh (VPS deployment script)"
    echo ""
    echo "📁 Copy these files to your VPS and run deploy_vps.sh"
    echo ""
}

# Create VPS deployment files
create_vps_files() {
    echo "📝 Creating VPS deployment files..."
    
    # Create systemd service file
    cat > colligent.service << 'EOF'
[Unit]
Description=Colligent Streamlit App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/colligent
Environment="PATH=/home/ubuntu/colligent/venv/bin"
ExecStart=/home/ubuntu/colligent/venv/bin/streamlit run colligent_web_app.py --server.port 8501
Restart=always

[Install]
WantedBy=multi-user.target
EOF

    # Create Nginx configuration
    cat > nginx.conf << 'EOF'
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
EOF

    # Create VPS deployment script
    cat > deploy_vps.sh << 'EOF'
#!/bin/bash

echo "🚀 Deploying Colligent to VPS..."

# Update system
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy service file
sudo cp colligent.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable colligent
sudo systemctl start colligent

# Configure Nginx
sudo cp nginx.conf /etc/nginx/sites-available/colligent
sudo ln -sf /etc/nginx/sites-available/colligent /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

echo "✅ Deployment complete!"
echo "🌐 Your app should be running on port 8501"
echo "🔧 Check status with: sudo systemctl status colligent"
EOF

    chmod +x deploy_vps.sh
    echo "✅ VPS deployment files created!"
}

# Main menu
while true; do
    echo ""
    echo "🎯 Choose deployment option:"
    echo "1) Streamlit Cloud (Recommended - Free)"
    echo "2) Railway (Alternative - Free)"
    echo "3) Heroku (Paid - More Control)"
    echo "4) VPS/Cloud Server (Advanced - Full Control)"
    echo "5) Create VPS deployment files"
    echo "6) Exit"
    echo ""
    read -p "Enter your choice (1-6): " choice
    
    case $choice in
        1)
            deploy_streamlit
            ;;
        2)
            deploy_railway
            ;;
        3)
            deploy_heroku
            ;;
        4)
            deploy_vps
            ;;
        5)
            create_vps_files
            ;;
        6)
            echo "👋 Goodbye! Good luck with your deployment!"
            exit 0
            ;;
        *)
            echo "❌ Invalid choice. Please try again."
            ;;
    esac
    
    echo ""
    read -p "Press Enter to continue..."
done
