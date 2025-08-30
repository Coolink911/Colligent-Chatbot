#!/bin/bash

# Setup script for ColliGent custom domain
# This script configures http://colligent/ to point to your Streamlit app

echo "🔧 Setting up ColliGent custom domain..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run this script as root (use sudo)"
    exit 1
fi

# Install nginx if not installed
if ! command -v nginx &> /dev/null; then
    echo "📦 Installing nginx..."
    apt update
    apt install -y nginx
fi

# Copy nginx configuration
echo "📝 Configuring nginx..."
cp nginx_colligent.conf /etc/nginx/sites-available/colligent

# Create symlink
ln -sf /etc/nginx/sites-available/colligent /etc/nginx/sites-enabled/

# Remove default site
rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
if nginx -t; then
    echo "✅ Nginx configuration is valid"
else
    echo "❌ Nginx configuration error"
    exit 1
fi

# Restart nginx
systemctl restart nginx
systemctl enable nginx

# Add to hosts file
echo "📝 Adding colligent to /etc/hosts..."
if ! grep -q "colligent" /etc/hosts; then
    echo "127.0.0.1 colligent" >> /etc/hosts
fi

echo "✅ Setup complete!"
echo ""
echo "🌐 Your ColliGent app is now available at:"
echo "   http://colligent/"
echo ""
echo "🚀 To start the app, run:"
echo "   streamlit run colligent_web_app.py"
echo ""
echo "🔒 Security features enabled:"
echo "   - IP whitelist"
echo "   - Rate limiting"
echo "   - XSS protection"
echo "   - Session timeout"
