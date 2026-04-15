# Single Service Deployment Guide for AI Landing Page Personalizer

## Overview
This guide covers deploying the entire AI Landing Page Personalizer as a single service on Render.com using the unified render.yaml configuration.

## Prerequisites
- Render.com account
- Groq API key
- GitHub repository with the project code

## Quick Start - One Service Deployment

### 1. Push to GitHub
Ensure your project is pushed to a GitHub repository with the unified `render.yaml` file at the root.

### 2. Deploy as Single Service

#### Automatic Deployment with render.yaml:
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" -> "Web Service"
3. Connect your GitHub repository
4. Select the **root directory** (not backend or frontend subdirectories)
5. Render will automatically detect and use the root `render.yaml`

#### What Happens Automatically:
- **Backend**: Python dependencies installed from `backend/requirements.txt`
- **Frontend**: Node dependencies installed and React app built to `frontend/build`
- **Static Files**: Frontend build files served as static content
- **API Server**: FastAPI backend runs on the same service

### 3. Environment Variables
Set these environment variables in your Render service:

#### Required Variables:
```
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=postgresql://user:password@host:port/dbname
```

#### Optional Variables (already configured):
```
CORS_ORIGINS=*
GENERATED_PAGES_DIR=generated_pages
ENVIRONMENT=production
REACT_APP_API_URL=
```

### 4. Database Setup
1. In Render Dashboard, click "New +" -> "PostgreSQL"
2. Name: `autowebsite-db`
3. Plan: Free
4. After creation, copy the connection string
5. Add it to your service environment variables as `DATABASE_URL`

### 5. How It Works

#### Service Architecture:
```
Single Render Service (Node Runtime)
    |
    |-- Backend API (FastAPI on port $PORT)
    |-- Frontend Static Files (React build)
    |-- Generated Pages (/generated/*)
```

#### Request Flow:
1. **Frontend Pages**: Served as static files from `/frontend/build`
2. **API Requests**: Handled by FastAPI backend
3. **Generated Pages**: Served from `/generated` directory
4. **File Uploads**: Processed by backend endpoints

### 6. Testing Your Deployment

#### Health Check:
- Visit: `https://your-service.onrender.com/health`
- Should return: `{"status": "healthy", "timestamp": "..."}`

#### Full Application Test:
1. Visit your service URL
2. Upload an ad creative (image, URL, or text)
3. Enter a landing page URL
4. Click "Generate Personalized Page"
5. View the results and generated page

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GROQ_API_KEY` | Yes | - | Your Groq API key for AI processing |
| `DATABASE_URL` | Yes | - | PostgreSQL connection string |
| `CORS_ORIGINS` | No | `*` | Allowed origins for CORS |
| `GENERATED_PAGES_DIR` | No | `generated_pages` | Directory for generated pages |
| `ENVIRONMENT` | No | `production` | Environment setting |
| `REACT_APP_API_URL` | No | `""` | Frontend API URL (empty for same service) |

## Troubleshooting

### Common Issues:

#### 1. Build Fails
```
Error: Build command failed
```
**Solution**: Check build logs, verify all dependencies are correct

#### 2. Frontend Not Loading
```
Error: Cannot GET /
```
**Solution**: Ensure frontend build completed successfully

#### 3. API Not Responding
```
Error: 502 Bad Gateway
```
**Solution**: Check backend startup logs, verify FastAPI is running

#### 4. Database Connection
```
Error: could not connect to server
```
**Solution**: Verify DATABASE_URL is correct and PostgreSQL is running

#### 5. Groq API Issues
```
Error: The api_key client option must be set
```
**Solution**: Ensure GROQ_API_KEY is set correctly

### Debugging Steps:

1. **Check Build Logs**: Service -> "Logs" -> Build tab
2. **Check Runtime Logs**: Service -> "Logs" -> Runtime tab
3. **Test Health Endpoint**: Visit `/health` endpoint
4. **Verify Environment**: Service -> "Environment" tab

## Advantages of Single Service

### Benefits:
- **Simpler Setup**: One service to configure and manage
- **No CORS Issues**: Frontend and backend on same domain
- **Cost Effective**: Only one service running
- **Easier Debugging**: Single set of logs to check
- **Faster Deployment**: One deployment process

### Trade-offs:
- **Less Scalability**: Frontend and backend share resources
- **Shared Downtime**: If backend fails, frontend also unavailable
- **Build Complexity**: Both frontend and backend build together

## Scaling Considerations

### When to Upgrade:
- High traffic (multiple simultaneous users)
- Large file uploads
- Frequent API calls to Groq
- Database storage limits reached

### Scaling Options:
1. **Upgrade Instance**: Move to Standard or Pro plan
2. **Separate Services**: Split into backend/frontend for better scaling
3. **Database Upgrade**: Upgrade PostgreSQL plan

## Local Development

### Run Locally:
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (in separate terminal)
cd frontend
npm install
npm start
```

### Environment Files:
```bash
# Backend
cp backend/.env.example backend/.env

# Frontend  
cp frontend/.env.example frontend/.env
```

## Security Best Practices

1. **API Keys**: Never commit API keys to Git
2. **HTTPS**: All services automatically use HTTPS on Render
3. **Input Validation**: All inputs validated in backend
4. **File Security**: Uploaded files processed safely

## Cost Optimization

### Free Tier Includes:
- 750 hours/month compute time
- 100GB bandwidth/month
- Static file serving
- Basic monitoring

### Optimization Tips:
1. Implement caching for repeated requests
2. Optimize image uploads (compress images)
3. Use efficient database queries
4. Monitor API usage closely

## Custom Domain (Optional)

1. In Render Dashboard, go to your service settings
2. Click "Custom Domains"
3. Add your custom domain
4. Update DNS records as instructed by Render

## Support

### Render Documentation:
- [Render Docs](https://render.com/docs)
- [Render Community](https://community.render.com)

### Common Issues:
- Check Render status page for outages
- Review deployment logs
- Test locally before deploying

This single-service deployment provides a simple, cost-effective way to run your AI Landing Page Personalizer with minimal configuration overhead.
