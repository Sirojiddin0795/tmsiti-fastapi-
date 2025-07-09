from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
from app.db.database import Base

class Law(Base):
    __tablename__ = "laws"
    
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), nullable=False)
    
    # Multilingual content
    name_uz = Column(String(500), nullable=False)
    name_ru = Column(String(500), nullable=False)
    name_en = Column(String(500), nullable=False)
    
    adoption_date = Column(DateTime(timezone=True), nullable=False)
    effective_date = Column(DateTime(timezone=True), nullable=False)
    
    # Multilingual authority
    authority_uz = Column(String(255), nullable=False)
    authority_ru = Column(String(255), nullable=False)
    authority_en = Column(String(255), nullable=False)
    
    lex_uz_link = Column(String(500), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class UrbanNorm(Base):
    __tablename__ = "urban_norms"
    
    id = Column(Integer, primary_key=True, index=True)
    document_code = Column(String(50), nullable=False, unique=True)
    
    # Multilingual content
    name_uz = Column(String(500), nullable=False)
    name_ru = Column(String(500), nullable=False)
    name_en = Column(String(500), nullable=False)
    
    lex_uz_link = Column(String(500), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Standard(Base):
    __tablename__ = "standards"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Multilingual content
    name_uz = Column(String(500), nullable=False)
    name_ru = Column(String(500), nullable=False)
    name_en = Column(String(500), nullable=False)
    
    pdf_path = Column(String(255), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class BuildingRegulation(Base):
    __tablename__ = "building_regulations"
    
    id = Column(Integer, primary_key=True, index=True)
    document_number = Column(String(50), nullable=False)
    designation = Column(String(100), nullable=False)
    
    # Multilingual content
    name_uz = Column(String(500), nullable=False)
    name_ru = Column(String(500), nullable=False)
    name_en = Column(String(500), nullable=False)
    
    pdf_path = Column(String(255), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class SmetaResourceNorm(Base):
    __tablename__ = "smeta_resource_norms"
    
    id = Column(Integer, primary_key=True, index=True)
    document_number = Column(String(50), nullable=False)
    shnq_number = Column(String(50), nullable=False)
    
    # Multilingual content
    shnq_name_uz = Column(String(500), nullable=False)
    shnq_name_ru = Column(String(500), nullable=False)
    shnq_name_en = Column(String(500), nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Reference(Base):
    __tablename__ = "references"
    
    id = Column(Integer, primary_key=True, index=True)
    reference_number = Column(String(50), nullable=False)
    
    # Multilingual content
    name_uz = Column(String(500), nullable=False)
    name_ru = Column(String(500), nullable=False)
    name_en = Column(String(500), nullable=False)
    
    pdf_path = Column(String(255), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
