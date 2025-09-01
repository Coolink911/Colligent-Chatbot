# 🦄 Deploy Colligent on Heroku

Heroku provides professional hosting with custom domains and scaling options.

## Prerequisites:
- Heroku account (free tier available)
- Heroku CLI installed

## Steps:

1. **Install Heroku CLI**:
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login to Heroku**:
   ```bash
   heroku login
   ```

3. **Create Heroku App**:
   ```bash
   heroku create your-colligent-app
   ```

4. **Set Environment Variables**:
   ```bash
   heroku config:set OPENAI_API_KEY=your_api_key_here
   heroku config:set OPENAI_MODEL=gpt-3.5-turbo
   ```

5. **Deploy**:
   ```bash
   git push heroku main
   ```

6. **Open App**:
   ```bash
   heroku open
   ```

## Custom Domain:
- Add domain in Heroku dashboard
- SSL certificate included
- Professional URL (e.g., `colligent.yourdomain.com`)

## Benefits:
- ✅ Professional hosting
- ✅ Custom domains
- ✅ SSL certificates
- ✅ Scaling options
- ✅ Monitoring and logs
