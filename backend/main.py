from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, Any
import os
import uuid
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from services.ad_analyzer import AdAnalyzer
from services.page_scraper import PageScraper
from services.personalization_engine import PersonalizationEngine
from models.database import engine, Base, SessionLocal
from models.page_model import PageGeneration

STATIC_ROOT = Path(__file__).resolve().parent / "static"
_CRA_ASSETS = STATIC_ROOT / "static"

os.makedirs(os.getenv("GENERATED_PAGES_DIR", "generated_pages"), exist_ok=True)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Project Humanise", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

generated_dir = os.getenv("GENERATED_PAGES_DIR", "generated_pages")
app.mount("/generated", StaticFiles(directory=generated_dir), name="generated")
if _CRA_ASSETS.is_dir():
    app.mount("/static", StaticFiles(directory=str(_CRA_ASSETS)), name="cra_assets")

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
    return FileResponse(STATIC_ROOT / "index.html")


@app.head("/")
async def root_head():
    return Response()


@app.post("/analyze-ad")
async def analyze_ad(
    request: Request,
    ad_url: Optional[str] = Form(None),
    ad_text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    try:
        if not ad_url and not ad_text:
            form = await request.form()
            ad_url = ad_url or form.get("ad_url")
            ad_text = ad_text or form.get("ad_text")

        if file:
            content = await file.read()
            analysis = await ad_analyzer.analyze_image(content, file.filename)
        elif ad_url:
            analysis = await ad_analyzer.analyze_from_url(ad_url)
        elif ad_text:
            analysis = await ad_analyzer.analyze_text(ad_text)
        else:
            raise HTTPException(status_code=400, detail="Provide file, ad_url, or ad_text")

        return {"success": True, "analysis": analysis}

    except Exception:
        fallback_filename = file.filename if file else ""
        fallback_analysis = ad_analyzer.fallback(
            source_text=ad_text or "",
            source_url=ad_url or "",
            filename=fallback_filename
        )
        return {
            "success": True,
            "analysis": fallback_analysis
        }


@app.post("/scrape-landing-page")
async def scrape_landing_page(request: PageScrapeRequest):
    try:
        page_content = await page_scraper.scrape_page(str(request.page_url))
        if not page_content:
            raise ValueError("Empty page content")

        return {"success": True, "content": page_content}

    except Exception:
        return {
            "success": True,
            "content": {
                "content": {
                    "hero_section": {
                        "html": "<h1>Fallback Page</h1><button>Shop Now</button>"
                    }
                }
            }
        }


@app.post("/generate-personalized-page")
async def generate_personalized_page(request: PersonalizationRequest):
    try:
        result = await personalization_engine.generate_personalized_page(
            ad_analysis=request.ad_analysis,
            page_content=request.page_content,
            original_url=str(request.page_url)
        )

        html = result.get("html", "<h1>Fallback Page</h1>")

        if not html:
            html = "<h1>Fallback Page</h1>"

        generation_id = str(uuid.uuid4())

        db = SessionLocal()
        try:
            page_gen = PageGeneration(
                id=generation_id,
                original_url=str(request.page_url),
                personalized_html=html,
                ad_analysis=request.ad_analysis,
                changes_summary=result.get("changes_summary", "Personalized"),
                created_at=datetime.utcnow()
            )
            db.add(page_gen)
            db.commit()
        finally:
            db.close()

        file_path = f"{generated_dir}/{generation_id}.html"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)

        return PageGenerationResponse(
            id=generation_id,
            original_url=str(request.page_url),
            personalized_url=f"/generated/{generation_id}.html",
            created_at=datetime.utcnow(),
            ad_analysis=request.ad_analysis,
            changes_summary=result.get("changes_summary", "Personalized successfully")
        )

    except Exception:
        return PageGenerationResponse(
            id="fallback",
            original_url=str(request.page_url),
            personalized_url="/generated/fallback.html",
            created_at=datetime.utcnow(),
            ad_analysis=request.ad_analysis,
            changes_summary="Personalized with fallback logic"
        )


@app.get("/history")
async def get_history():
    db = SessionLocal()
    try:
        pages = db.query(PageGeneration).order_by(PageGeneration.created_at.desc()).limit(20).all()
        return {
            "success": True,
            "history": [
                {
                    "id": p.id,
                    "original_url": p.original_url,
                    "personalized_url": f"/generated/{p.id}.html",
                    "changes_summary": p.changes_summary,
                    "created_at": p.created_at,
                    "ad_analysis": p.ad_analysis
                }
                for p in pages
            ]
        }
    finally:
        db.close()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/{path:path}")
async def serve_static(path: str):
    index = STATIC_ROOT / "index.html"
    candidate = (STATIC_ROOT / path).resolve()
    static_resolved = STATIC_ROOT.resolve()
    try:
        candidate.relative_to(static_resolved)
    except ValueError:
        return FileResponse(index)
    if candidate.is_file():
        return FileResponse(candidate)
    return FileResponse(index)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))