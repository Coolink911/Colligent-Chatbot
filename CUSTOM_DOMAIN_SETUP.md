# 🌐 ColliGent Custom Domain Setup

This guide will help you set up `http://colligent/` as your personalized URL for the ColliGent chatbot.

## 🔧 Quick Setup

### **Option 1: Automated Setup (Recommended)**
```bash
# Run the setup script as root
sudo ./setup_colligent_domain.sh
```

### **Option 2: Manual Setup**

#### **Step 1: Install Nginx**
```bash
sudo apt update
sudo apt install nginx
```

#### **Step 2: Configure Nginx**
```bash
# Copy the configuration file
sudo cp nginx_colligent.conf /etc/nginx/sites-available/colligent

# Create symlink
sudo ln -sf /etc/nginx/sites-available/colligent /etc/nginx/sites-enabled/

# Remove default site
sudo rm -f /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
sudo systemctl enable nginx
```

#### **Step 3: Add to Hosts File**
```bash
# Add colligent to /etc/hosts
echo "127.0.0.1 colligent" | sudo tee -a /etc/hosts
```

## 🚀 Start the Application

```bash
# Start ColliGent
streamlit run colligent_web_app.py
```

## 🌐 Access Your App

Once setup is complete, access your ColliGent chatbot at:
**http://colligent/**

## 🔒 Security Features Enabled

### **Network Security**
- **IP Whitelist**: Only authorized IPs can access
- **Rate Limiting**: 10 requests per minute per IP
- **Security Headers**: XSS protection, content type validation
- **File Access Control**: Blocks access to sensitive files

### **Application Security**
- **Input Validation**: Prevents XSS and injection attacks
- **Session Timeout**: 30-minute session limits
- **Output Sanitization**: Removes malicious content
- **Suspicious Activity Logging**: Monitors for abuse

### **Configuration Security**
- **Environment Variables**: Secure API key management
- **Reduced Limits**: Smaller upload sizes and message limits
- **CORS Protection**: Disabled for local deployment
- **XSRF Protection**: Enabled for form security

## 🛠️ Troubleshooting

### **If colligent/ doesn't work:**
1. Check if nginx is running: `sudo systemctl status nginx`
2. Check nginx logs: `sudo tail -f /var/log/nginx/error.log`
3. Verify hosts file: `cat /etc/hosts | grep colligent`
4. Test nginx config: `sudo nginx -t`

### **If you get access denied:**
1. Check your IP is in the whitelist in `colligent_config.py`
2. Add your IP to `ALLOWED_IPS` list
3. Restart the Streamlit application

### **If rate limited:**
1. Wait 1 minute before trying again
2. Check the rate limit settings in `colligent_config.py`
3. Adjust `MAX_REQUESTS_PER_MINUTE` if needed

## 📝 Customization

### **Change Domain Name**
To use a different domain (e.g., `http://myai/`):

1. Edit `nginx_colligent.conf`:
   ```nginx
   server_name myai localhost;
   ```

2. Update `/etc/hosts`:
   ```
   127.0.0.1 myai
   ```

3. Restart nginx:
   ```bash
   sudo systemctl restart nginx
   ```

### **Add More IPs to Whitelist**
Edit `colligent_config.py`:
```python
ALLOWED_IPS = ["127.0.0.1", "localhost", "192.168.1.149", "YOUR_IP_HERE"]
```

## 🎯 Benefits

- **Professional URL**: `http://colligent/` instead of `http://localhost:8501`
- **Enhanced Security**: Multiple layers of protection
- **Better Performance**: Nginx proxy with caching
- **Production Ready**: Enterprise-level security features
