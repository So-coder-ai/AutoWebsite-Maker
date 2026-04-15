# Deployment Guide for AI Landing Page Personalizer

## Overview
This guide covers deploying the AI Landing Page Personalizer on Render.com with separate backend and frontend services using the updated render.yaml configuration files.

## Prerequisites
- Render.com account
- Groq API key (not OpenAI)
- GitHub repository with the project code

## Quick Start (Using render.yaml Files)

### 1. Push to GitHub
Ensure your project is pushed to a GitHub repository with the following structure:
```
AutoWebsite-Maker/
  backend/
    main.py
    requirements.txt
    render.yaml
    services/
    models/
  frontend/
    src/
    package.json
    render.yaml
    .env.example
```

### 2. Backend Deployment (FastAPI)

#### Automatic Deployment with render.yaml:
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" -> "Web Service"
3. Connect your GitHub repository
4. Select the `backend` folder as root directory
5. Render will automatically detect and use `render.yaml`

#### Manual Configuration (if needed):
- **Name**: `autowebsite-backend`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Instance Type**: `Free` (or upgrade as needed)

#### Environment Variables for Backend:
```
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=postgresql://user:password@host:port/dbname
CORS_ORIGINS=https://your-frontend-domain.onrender.com
GENERATED_PAGES_DIR=generated_pages
ENVIRONMENT=production
```

#### Database Setup:
1. In Render Dashboard, click "New +" -> "PostgreSQL"
2. Name: `landing-page-db`
3. Plan: Free
4. After creation, copy the connection string from the database page
5. Add it to your backend environment variables as `DATABASE_URL`

### 3. Frontend Deployment (React)

#### Automatic Deployment with render.yaml:
1. Go to Render Dashboard
2. Click "New +" -> "Web Service"
3. Connect your GitHub repository
4. Select the `frontend` folder as root directory
5. Render will automatically detect and use `render.yaml`

#### Manual Configuration (if needed):
- **Name**: `autowebsite-frontend`
- **Environment**: `Node`
- **Build Command**: `npm install && npm run build`
- **Publish Directory**: `build`
- **Instance Type**: `Static`

#### Environment Variables for Frontend:
```
REACT_APP_API_URL=https://your-backend-domain.onrender.com
```

### 4. Post-Deployment Steps

#### Update CORS Origins:
1. Get your frontend URL from Render dashboard
2. Update backend `CORS_ORIGINS` environment variable:
```
CORS_ORIGINS=https://your-frontend-domain.onrender.com
```

#### Test the Application:
1. Visit your frontend URL
2. Test ad upload and analysis
3. Test landing page personalization
4. Verify generated pages are accessible via `/generated/{id}.html`

## Key Changes for This Version

### Backend Improvements:
- **Groq Integration**: Uses Groq API instead of OpenAI
- **Async Scraping**: Fixed blocking calls with httpx
- **Graceful Selenium**: Degrades gracefully without Chrome
- **Database Fixes**: Properly saves PageGeneration records
- **History Endpoint**: New `/history` endpoint for recent generations
- **Error Handling**: Better HTTP error propagation
- **Logging**: Added logging for JSON parse failures

### Frontend Improvements:
- **API Configuration**: Uses environment variable for API URL
- **Render Compatibility**: Proper static site configuration

### Render Configuration:
- **Port Handling**: Uses `$PORT` environment variable
- **Directory Structure**: Proper root directory configuration
- **Environment Variables**: All required variables documented

## Environment Variables Reference

### Backend Variables:
| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | Yes | Your Groq API key |
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `CORS_ORIGINS` | Yes | Allowed origins for CORS |
| `GENERATED_PAGES_DIR` | No | Directory for generated pages (default: generated_pages) |
| `ENVIRONMENT` | No | Environment (default: production) |

### Frontend Variables:
| Variable | Required | Description |
|----------|----------|-------------|
| `REACT_APP_API_URL` | Yes | Backend API URL |

## Troubleshooting

### Common Issues:

#### 1. CORS Errors
```
Error: Access to fetch at 'https://backend.onrender.com' from origin 'https://frontend.onrender.com' has been blocked by CORS policy
```
**Solution**: Ensure `CORS_ORIGINS` includes your frontend URL exactly

#### 2. Database Connection Issues
```
Error: OperationalError: could not connect to server
```
**Solution**: Verify `DATABASE_URL` is correctly set and PostgreSQL service is running

#### 3. Groq API Errors
```
Error: The api_key client option must be set
```
**Solution**: Ensure `GROQ_API_KEY` is set correctly in backend environment

#### 4. Build Failures
**Solution**: Check build logs in Render Dashboard, verify all dependencies in requirements.txt

#### 5. File Upload Issues
**Solution**: Ensure file sizes are within limits, check content-type headers

### Debugging Steps:

1. **Check Logs**: Go to service -> "Logs" in Render Dashboard
2. **Test Health Endpoint**: Visit `https://your-backend.onrender.com/health`
3. **Verify Environment Variables**: Check service -> "Environment" tab
4. **Test API Directly**: Use curl or Postman to test endpoints

## Monitoring and Maintenance

### Health Checks:
- Backend: `/health` endpoint (automatically monitored by Render)
- Frontend: Static site health check

### Log Monitoring:
- Backend logs: Available in Render Dashboard
- Frontend logs: Available in Render Dashboard
- Database logs: Available in PostgreSQL service page

### Performance Monitoring:
- Render provides basic metrics on the dashboard
- Monitor response times and error rates

## Scaling Considerations

### When to Upgrade:
- High traffic (multiple simultaneous users)
- Large file uploads
- Frequent API calls to Groq
- Database storage limits reached

### Scaling Options:
1. **Backend**: Upgrade to Standard or Pro instance
2. **Database**: Upgrade PostgreSQL plan
3. **Frontend**: Usually fine on Free tier (static hosting)

## Security Best Practices

1. **API Keys**: Never commit API keys to Git
2. **HTTPS**: All services automatically use HTTPS on Render
3. **Rate Limiting**: Consider implementing rate limiting for API endpoints
4. **Input Validation**: All inputs are validated in the backend
5. **File Security**: Uploaded files are processed safely

## Cost Optimization

### Free Tier Limitations:
- 750 hours/month compute time
- 100GB bandwidth/month
- Limited database connections
- No custom domains on free tier

### Optimization Tips:
1. Implement caching for repeated requests
2. Optimize image uploads (compress images)
3. Use efficient database queries
4. Monitor API usage closely

## Custom Domain Setup (Optional)

1. In Render Dashboard, go to your service settings
2. Click "Custom Domains"
3. Add your custom domain
4. Update DNS records as instructed by Render
5. Update CORS origins if needed

## Support

### Render Documentation:
- [Render Docs](https://render.com/docs)
- [Render Community](https://community.render.com)

### Common Issues:
- Check Render status page for outages
- Review deployment logs
- Test locally before deploying

## Local Development Setup

### Backend:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend:
```bash
cd frontend
npm install
npm start
```

### Environment Files:
- Copy `backend/.env.example` to `backend/.env`
- Copy `frontend/.env.example` to `frontend/.env`
- Fill in your API keys and URLs

This deployment setup provides a production-ready environment for your AI Landing Page Personalizer with automatic scaling, monitoring, and maintenance using the updated render.yaml configuration files.
