# 🤖 Colligent Test App

This is a simplified test version of the Colligent chatbot to debug deployment issues.

## 🚀 Quick Start

### Local Testing
1. **Install dependencies**:
   ```bash
   pip install -r requirements-test.txt
   ```

2. **Run tests**:
   ```bash
   python test_local.py
   ```

3. **Run app locally**:
   ```bash
   streamlit run test_app.py --server.port=8501
   ```

### Render Deployment
1. **Go to**: [render.com](https://render.com)
2. **Click**: "New +" → "Web Service"
3. **Connect**: This GitHub repo
4. **Configure**:
   - **Name**: `colligent-test-app`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements-test.txt`
   - **Start Command**: `streamlit run test_app.py --server.port=$PORT --server.address=0.0.0.0`
5. **Click**: "Create Web Service"

## 📁 Files

- **`test_app.py`**: Minimal Streamlit app for testing
- **`requirements-test.txt`**: Minimal dependencies
- **`render-test.yaml`**: Render deployment config
- **`test_local.py`**: Local testing script

## 🔍 What This Tests

- ✅ **Basic Streamlit functionality**
- ✅ **Session state management**
- ✅ **File system access**
- ✅ **Environment variables**
- ✅ **Package imports**
- ✅ **Simple chat interface**

## 🎯 Purpose

This simplified app helps identify whether deployment issues are:
- **Streamlit-specific**: If this fails, it's a Streamlit deployment issue
- **Dependency-related**: If this works but main app fails, it's a package issue
- **Configuration-related**: If this works locally but not on Render, it's a config issue

## 🚨 Troubleshooting

If the test app fails:
1. Check `test_local.py` output
2. Verify package versions
3. Check Python version compatibility
4. Review Render logs

If the test app works but main app fails:
1. Compare requirements files
2. Check import dependencies
3. Review error logs
4. Test individual modules
