# 🚀 Heroku Deployment Guide for Test App

## Prerequisites
1. **Heroku CLI installed**: Download from [heroku.com/cli](https://heroku.com/cli)
2. **Git repository**: Your code should be in a Git repo
3. **Heroku account**: Sign up at [heroku.com](https://heroku.com)

## 🚀 Quick Deployment

### 1. Install Heroku CLI
```bash
# Ubuntu/Debian
curl https://cli-assets.heroku.com/install-ubuntu.sh | sh

# Or download from heroku.com/cli
```

### 2. Login to Heroku
```bash
heroku login
```

### 3. Create Heroku App
```bash
# From your project directory
heroku create colligent-test-app
```

### 4. Set Buildpacks
```bash
heroku buildpacks:set heroku/python
```

### 5. Deploy
```bash
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku main
```

### 6. Open App
```bash
heroku open
```

## 📁 Required Files

- **`Procfile`**: Tells Heroku how to run your app
- **`requirements-heroku.txt`**: Python dependencies
- **`runtime.txt`**: Python version
- **`setup.sh`**: Configuration setup script

## 🔧 Configuration

### Environment Variables
```bash
heroku config:set PORT=10000
heroku config:set PYTHON_VERSION=3.11.7
```

### Buildpacks
```bash
heroku buildpacks:set heroku/python
```

## 🚨 Troubleshooting

### Common Issues
1. **Build fails**: Check `requirements-heroku.txt` syntax
2. **App crashes**: Check logs with `heroku logs --tail`
3. **Port issues**: Ensure `$PORT` is used in Procfile

### View Logs
```bash
heroku logs --tail
```

### Restart App
```bash
heroku restart
```

## 🌐 Alternative: Heroku Dashboard

1. Go to [dashboard.heroku.com](https://dashboard.heroku.com)
2. Click "New" → "Create new app"
3. Connect your GitHub repo
4. Deploy from GitHub

## 📊 Monitoring

- **Logs**: `heroku logs --tail`
- **Status**: `heroku ps`
- **Info**: `heroku info`
