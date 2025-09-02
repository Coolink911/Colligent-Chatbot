#!/bin/bash

# Startup script for Render deployment
echo "Starting Colligent app on Render..."

# Set environment variables
export PORT=${PORT:-10000}
export PYTHONPATH=/app

# Create Streamlit config directory if it doesn't exist
mkdir -p ~/.streamlit

# Create Streamlit config for Render
cat > ~/.streamlit/config.toml << EOF
[global]
developmentMode = false

[server]
headless = true
enableCORS = false
enableXsrfProtection = false
port = $PORT
address = "0.0.0.0"

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = false
EOF

echo "Streamlit config created with port: $PORT"
echo "Starting Streamlit app..."

# Start the app
exec streamlit run colligent_web_app.py --server.port=$PORT --server.address=0.0.0.0
