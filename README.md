# AI-Powered Landing Page Personalizer

This project is a web application that personalizes landing pages based on the content of an ad.  
The goal is to improve how well a landing page matches the message of an ad, which is important for user experience and conversions.

---

## What the project does

The application takes:

- An ad (text, image, or URL)
- A landing page URL

It then:

1. Extracts key information from the ad (headline, tone, call-to-action, etc.)
2. Scrapes the landing page
3. Modifies parts of the page (like headline and buttons)
4. Generates a personalized version of the same page

The important part is that it keeps the original layout and only changes content where needed.

---

## Tech Stack

- Backend: FastAPI (Python)
- Frontend: React (pre-built and served as static files)
- Web Scraping: Playwright
- HTML Parsing: BeautifulSoup
- AI (optional): Gemini API  
- Fallback logic: Rule-based (used when AI is unavailable)
- Deployment: Render (Docker)

---

## How it works

1. The user provides an ad and a website URL  
2. The backend:
   - Analyzes the ad  
   - Loads the full website using Playwright  
   - Parses the HTML  
3. The system updates:
   - Headline  
   - CTA buttons  
   - Adds a simple banner  
4. A modified version of the page is returned  

---

## Features

- Works with real websites (including dynamic ones)
- Keeps original page structure intact
- Simple fallback logic if AI APIs are unavailable
- Generates a working personalized page instead of a mockup

---

## Running locally

### 1. Clone the repository

```bash
git clone <repo>
cd AutoWebsite-Maker
```

---

### 2. Backend setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

---

### 3. Frontend

The frontend is already built and stored in:

`backend/static/`

So no separate frontend setup is required.

---

## Deployment

The app is deployed on Render using Docker.

To avoid build issues on low-memory environments:

- The frontend is built locally
- The build files are copied into backend/static/
- The backend serves these files directly

This keeps deployment simple and reliable.

---

## Live Demo

https://autowebsite-maker-1.onrender.com

---

## API Endpoints

- POST /analyze-ad  
- POST /scrape-landing-page  
- POST /generate-personalized-page  
- GET /generated/{id}.html  

---

## Notes

- AI usage is optional — the system still works with fallback logic
- Some complex websites may not fully render as expected
- The project focuses more on the concept than full production readiness

---

## License

MIT License
