from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
from app.db.database import Base

class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # User info
    full_name = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    
    # Message
    subject = Column(String(255), nullable=True)
    message = Column(Text, nullable=False)
    
    # Status
    is_read = Column(Boolean, default=False)
    is_replied = Column(Boolean, default=False)
    
    # Response
    admin_response = Column(Text, nullable=True)
    responded_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class AntiCorruption(Base):
    __tablename__ = "anti_corruption"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Multilingual content
    content_uz = Column(Text, nullable=False)
    content_ru = Column(Text, nullable=False)
    content_en = Column(Text, nullable=False)
    
    # Contact info
    contact_phone = Column(String(20), nullable=True)
    contact_email = Column(String(100), nullable=True)
    
    # Additional info
    hotline_uz = Column(String(255), nullable=True)
    hotline_ru = Column(String(255), nullable=True)
    hotline_en = Column(String(255), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
