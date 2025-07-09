from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
from app.db.database import Base

class About(Base):
    __tablename__ = "about"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Multilingual content
    content_uz = Column(Text, nullable=False)
    content_ru = Column(Text, nullable=False)
    content_en = Column(Text, nullable=False)
    
    # Certificate document
    certificate_pdf_path = Column(String(255), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Management(Base):
    __tablename__ = "management"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Personal info
    full_name_uz = Column(String(255), nullable=False)
    full_name_ru = Column(String(255), nullable=False)
    full_name_en = Column(String(255), nullable=False)
    
    # Position
    position_uz = Column(String(255), nullable=False)
    position_ru = Column(String(255), nullable=False)
    position_en = Column(String(255), nullable=False)
    
    # Contact info
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    
    # Reception days
    reception_days_uz = Column(String(255), nullable=True)
    reception_days_ru = Column(String(255), nullable=True)
    reception_days_en = Column(String(255), nullable=True)
    
    # Bio/Description
    bio_uz = Column(Text, nullable=True)
    bio_ru = Column(Text, nullable=True)
    bio_en = Column(Text, nullable=True)
    
    # Photo
    photo_path = Column(String(255), nullable=True)
    
    # Order for display
    display_order = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Structure(Base):
    __tablename__ = "structure"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Multilingual content
    content_uz = Column(Text, nullable=False)
    content_ru = Column(Text, nullable=False)
    content_en = Column(Text, nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class StructuralDivision(Base):
    __tablename__ = "structural_divisions"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Personal info
    full_name_uz = Column(String(255), nullable=False)
    full_name_ru = Column(String(255), nullable=False)
    full_name_en = Column(String(255), nullable=False)
    
    # Position
    position_uz = Column(String(255), nullable=False)
    position_ru = Column(String(255), nullable=False)
    position_en = Column(String(255), nullable=False)
    
    # Department
    department_uz = Column(String(255), nullable=False)
    department_ru = Column(String(255), nullable=False)
    department_en = Column(String(255), nullable=False)
    
    # Contact info
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    
    # Bio/Description
    bio_uz = Column(Text, nullable=True)
    bio_ru = Column(Text, nullable=True)
    bio_en = Column(Text, nullable=True)
    
    # Photo
    photo_path = Column(String(255), nullable=True)
    
    # Order for display
    display_order = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Vacancy(Base):
    __tablename__ = "vacancies"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Position
    position_uz = Column(String(255), nullable=False)
    position_ru = Column(String(255), nullable=False)
    position_en = Column(String(255), nullable=False)
    
    # Department
    department_uz = Column(String(255), nullable=False)
    department_ru = Column(String(255), nullable=False)
    department_en = Column(String(255), nullable=False)
    
    # Requirements
    requirements_uz = Column(Text, nullable=False)
    requirements_ru = Column(Text, nullable=False)
    requirements_en = Column(Text, nullable=False)
    
    # Status
    vacancy_status_uz = Column(String(100), nullable=False)
    vacancy_status_ru = Column(String(100), nullable=False)
    vacancy_status_en = Column(String(100), nullable=False)
    
    # Additional info
    salary_range = Column(String(100), nullable=True)
    deadline = Column(DateTime(timezone=True), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
