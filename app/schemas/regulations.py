from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LawBase(BaseModel):
    order_number: str
    name_uz: str
    name_ru: str
    name_en: str
    adoption_date: datetime
    effective_date: datetime
    authority_uz: str
    authority_ru: str
    authority_en: str
    lex_uz_link: Optional[str] = None

class LawCreate(LawBase):
    pass

class LawUpdate(BaseModel):
    order_number: Optional[str] = None
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    adoption_date: Optional[datetime] = None
    effective_date: Optional[datetime] = None
    authority_uz: Optional[str] = None
    authority_ru: Optional[str] = None
    authority_en: Optional[str] = None
    lex_uz_link: Optional[str] = None
    is_active: Optional[bool] = None

class Law(LawBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        orm_mode = True

class UrbanNormBase(BaseModel):
    document_code: str
    name_uz: str
    name_ru: str
    name_en: str
    lex_uz_link: Optional[str] = None

class UrbanNormCreate(UrbanNormBase):
    pass

class UrbanNormUpdate(BaseModel):
    document_code: Optional[str] = None
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    lex_uz_link: Optional[str] = None
    is_active: Optional[bool] = None

class UrbanNorm(UrbanNormBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        orm_mode = True

class StandardBase(BaseModel):
    name_uz: str
    name_ru: str
    name_en: str

class StandardCreate(StandardBase):
    pass

class StandardUpdate(BaseModel):
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    is_active: Optional[bool] = None

class Standard(StandardBase):
    id: int
    pdf_path: Optional[str] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        orm_mode = True

class BuildingRegulationBase(BaseModel):
    document_number: str
    designation: str
    name_uz: str
    name_ru: str
    name_en: str

class BuildingRegulationCreate(BuildingRegulationBase):
    pass

class BuildingRegulationUpdate(BaseModel):
    document_number: Optional[str] = None
    designation: Optional[str] = None
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    is_active: Optional[bool] = None

class BuildingRegulation(BuildingRegulationBase):
    id: int
    pdf_path: Optional[str] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        orm_mode = True

class SmetaResourceNormBase(BaseModel):
    document_number: str
    shnq_number: str
    shnq_name_uz: str
    shnq_name_ru: str
    shnq_name_en: str

class SmetaResourceNormCreate(SmetaResourceNormBase):
    pass

class SmetaResourceNormUpdate(BaseModel):
    document_number: Optional[str] = None
    shnq_number: Optional[str] = None
    shnq_name_uz: Optional[str] = None
    shnq_name_ru: Optional[str] = None
    shnq_name_en: Optional[str] = None
    is_active: Optional[bool] = None

class SmetaResourceNorm(SmetaResourceNormBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        orm_mode = True

class ReferenceBase(BaseModel):
    reference_number: str
    name_uz: str
    name_ru: str
    name_en: str

class ReferenceCreate(ReferenceBase):
    pass

class ReferenceUpdate(BaseModel):
    reference_number: Optional[str] = None
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    is_active: Optional[bool] = None

class Reference(ReferenceBase):
    id: int
    pdf_path: Optional[str] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        orm_mode = True
