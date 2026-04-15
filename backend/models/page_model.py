from sqlalchemy import Column, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from models.database import Base
import uuid

class PageGeneration(Base):
    __tablename__ = "page_generations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    original_url = Column(String, nullable=False)
    personalized_html = Column(Text, nullable=False)
    ad_analysis = Column(JSON, nullable=False)
    changes_summary = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
