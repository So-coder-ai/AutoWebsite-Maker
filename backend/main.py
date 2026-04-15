from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, Any, List
import os
import uuid
from datetime import datetime

from services.ad_analyzer import AdAnalyzer
from services.page_scraper import PageScraper
from services.personalization_engine import PersonalizationEngine
from models.database import engine, Base, SessionLocal
from models.page_model import PageGeneration

os.makedirs(os.getenv("GENERATED_PAGES_DIR", "generated_pages"), exist_ok=True)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Landing Page Personalizer", version="1.0.0")

allowed_origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

generated_dir = os.getenv("GENERATED_PAGES_DIR", "generated_pages")
app.mount("/generated", StaticFiles(directory=generated_dir), name="generated")

class AdAnalysisRequest(BaseModel):
    ad_url: Optional[HttpUrl] = None
    ad_text: Optional[str] = None

class PageScrapeRequest(BaseModel):
    page_url: HttpUrl

class PersonalizationRequest(BaseModel):
    ad_analysis: Dict[str, Any]
    page_content: Dict[str, Any]
    page_url: HttpUrl

class PageGenerationResponse(BaseModel):
    id: str
    original_url: str
    personalized_url: str
    created_at: datetime
    ad_analysis: Dict[str, Any]
    changes_summary: str

ad_analyzer = AdAnalyzer()
page_scraper = PageScraper()
personalization_engine = PersonalizationEngine()

@app.get("/")
async def root():
    return {"message": "AI Landing Page Personalizer API"}

@app.post("/analyze-ad")
async def analyze_ad(
    ad_url: Optional[str] = None,
    ad_text: Optional[str] = None,
    file: Optional[UploadFile] = File(None)
):
    try:
        if file:
            content = await file.read()
            analysis = await ad_analyzer.analyze_image(content, file.filename)
        elif ad_url:
            analysis = await ad_analyzer.analyze_from_url(ad_url)
        elif ad_text:
            analysis = await ad_analyzer.analyze_text(ad_text)
        else:
            raise HTTPException(
                status_code=400, 
                detail="Must provide either file, ad_url, or ad_text"
            )
        
        return {"success": True, "analysis": analysis}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scrape-landing-page")
async def scrape_landing_page(request: PageScrapeRequest):
    try:
        page_content = await page_scraper.scrape_page(str(request.page_url))
        return {"success": True, "content": page_content}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-personalized-page")
async def generate_personalized_page(request: PersonalizationRequest):
    try:
        personalized_content = await personalization_engine.generate_personalized_page(
            ad_analysis=request.ad_analysis,
            page_content=request.page_content,
            original_url=str(request.page_url)
        )
        
        generation_id = str(uuid.uuid4())
        page_gen = PageGeneration(
            id=generation_id,
            original_url=str(request.page_url),
            personalized_html=personalized_content["html"],
            ad_analysis=request.ad_analysis,
            changes_summary=personalized_content["changes_summary"],
            created_at=datetime.utcnow()
        )
        
        db = SessionLocal()
        try:
            db.add(page_gen)
            db.commit()
            db.refresh(page_gen)
        finally:
            db.close()
        
        generated_dir = os.getenv("GENERATED_PAGES_DIR", "generated_pages")
        os.makedirs(generated_dir, exist_ok=True)
        with open(f"{generated_dir}/{generation_id}.html", "w", encoding="utf-8") as f:
            f.write(personalized_content["html"])
        
        return PageGenerationResponse(
            id=generation_id,
            original_url=str(request.page_url),
            personalized_url=f"/generated/{generation_id}.html",
            created_at=datetime.utcnow(),
            ad_analysis=request.ad_analysis,
            changes_summary=personalized_content["changes_summary"]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/pages/{generation_id}")
async def get_page_generation(generation_id: str):
    try:
        generated_dir = os.getenv("GENERATED_PAGES_DIR", "generated_pages")
        file_path = f"{generated_dir}/{generation_id}.html"
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Page generation not found")
        
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        return {"html": html_content, "generation_id": generation_id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
async def get_history():
    try:
        db = SessionLocal()
        try:
            pages = db.query(PageGeneration).order_by(PageGeneration.created_at.desc()).limit(50).all()
            history = []
            for page in pages:
                history.append({
                    "id": page.id,
                    "original_url": page.original_url,
                    "personalized_url": f"/generated/{page.id}.html",
                    "changes_summary": page.changes_summary,
                    "created_at": page.created_at,
                    "ad_analysis": page.ad_analysis
                })
            return {"success": True, "history": history}
        finally:
            db.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
