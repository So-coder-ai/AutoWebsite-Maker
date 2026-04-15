# AI-Powered Landing Page Personalizer

A full-stack web application that creates personalized landing pages based on ad creatives and existing landing page URLs using AI-powered content optimization.

## Tech Stack

- **Frontend**: React + Tailwind CSS
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **AI**: OpenAI API for content generation
- **Deployment**: Vercel (frontend) + Render/Fly.io (backend)

## Core Features

1. **Ad Creative Analysis**: Extract headlines, tone, offers, and audience signals from uploaded images or links
2. **Landing Page Scraping**: Parse existing page structure, copy, and components
3. **AI Personalization**: Enhance existing pages with CRO principles while maintaining layout
4. **Live Preview**: Side-by-side comparison of original vs personalized pages
5. **Database Storage**: Track user inputs, outputs, and analytics

## System Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   React     │    │   FastAPI   │    │ PostgreSQL  │
│  Frontend   │◄──►│   Backend   │◄──►│  Database   │
└─────────────┘    └─────────────┘    └─────────────┘
                          │
                          ▼
                   ┌─────────────┐
                   │   OpenAI    │
                   │     API     │
                   └─────────────┘
```

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.9+
- PostgreSQL
- Groq API key
- Docker (optional, for containerized deployment)

### Local Development

1. **Clone and setup**:
   ```bash
   git clone <repository>
   cd AutoWebsite-Maker
   ```

2. **Backend setup**:
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env with your API keys and database URL
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

3. **Frontend setup**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Database setup**:
   ```bash
   createdb landing_page_personalizer
   # Run migrations from backend/
   ```

### Docker Development
```bash
# Start all services
docker-compose up --build

# Or start specific services
docker-compose up postgres redis
docker-compose up backend
docker-compose up frontend
```

## Quick Deploy to Render

### One-Click Deployment
1. Fork this repository
2. Connect to [Render](https://render.com)
3. Create two web services:
   - **Backend**: Point to `/backend` directory
   - **Frontend**: Point to `/frontend` directory
4. Add environment variables (see DEPLOYMENT.md)

### Manual Deployment
See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions.

## API Endpoints

- `POST /analyze-ad` - Analyze ad creative for key information
- `POST /scrape-landing-page` - Extract structure and content from URL
- `POST /generate-personalized-page` - Create enhanced landing page
- `GET /pages/{id}` - Retrieve saved page variations

## Key Features

### AI Personalization Engine
- Maintains existing layout structure
- Applies CRO best practices
- Ensures messaging consistency
- Prevents hallucinations through structured prompts

### Error Handling
- Graceful UI fallbacks
- Retry mechanisms for AI failures
- Output validation before rendering
- Consistent template-based generation

### Security
- Safe HTML rendering
- Input validation and sanitization
- Rate limiting on API endpoints
- Environment-based configuration

## Deployment

The application is designed for easy deployment:
- Frontend: Vercel (static files)
- Backend: Render/Fly.io (Docker container)
- Database: Managed PostgreSQL service

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details
