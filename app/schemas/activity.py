from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ManagementSystemBase(BaseModel):
    content_uz: str
    content_ru: str
    content_en: str

class ManagementSystemCreate(ManagementSystemBase):
    pass

class ManagementSystemUpdate(BaseModel):
    content_uz: Optional[str] = None
    content_ru: Optional[str] = None
    content_en: Optional[str] = None
    is_active: Optional[bool] = None

class ManagementSystem(ManagementSystemBase):
    id: int
    pdf_path: Optional[str] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        orm_mode = True

class LaboratoryBase(BaseModel):
    ksl_link: Optional[str] = "https://ksl.uz"
    description_uz: Optional[str] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None

class LaboratoryCreate(LaboratoryBase):
    pass

class LaboratoryUpdate(BaseModel):
    ksl_link: Optional[str] = None
    description_uz: Optional[str] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None
    is_active: Optional[bool] = None

class Laboratory(LaboratoryBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        orm_mode = True
