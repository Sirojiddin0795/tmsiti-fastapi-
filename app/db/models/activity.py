from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
from app.db.database import Base

class ManagementSystem(Base):
    __tablename__ = "management_systems"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Multilingual content
    content_uz = Column(Text, nullable=False)
    content_ru = Column(Text, nullable=False)
    content_en = Column(Text, nullable=False)
    
    # Document
    pdf_path = Column(String(255), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Laboratory(Base):
    __tablename__ = "laboratories"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Link to KSL.uz
    ksl_link = Column(String(500), default="https://ksl.uz")
    
    # Multilingual content
    description_uz = Column(Text, nullable=True)
    description_ru = Column(Text, nullable=True)
    description_en = Column(Text, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
