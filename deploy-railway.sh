#!/bin/bash

# 🚂 Railway Deployment Script for Colligent

echo "🚀 Deploying Colligent to Railway..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Login to Railway
echo "🔐 Logging into Railway..."
railway login

# Deploy the project
echo "🚀 Deploying to Railway..."
railway up

echo "✅ Deployment complete!"
echo "🌐 Your app should be available at the URL shown above"
echo "🔧 Don't forget to set environment variables in Railway dashboard:"
echo "   - OPENAI_API_KEY"
echo "   - OPENAI_MODEL=gpt-4o-mini"
