from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class AboutBase(BaseModel):
    content_uz: str
    content_ru: str
    content_en: str

class AboutCreate(AboutBase):
    pass

class AboutUpdate(BaseModel):
    content_uz: Optional[str] = None
    content_ru: Optional[str] = None
    content_en: Optional[str] = None
    is_active: Optional[bool] = None

class About(AboutBase):
    id: int
    certificate_pdf_path: Optional[str] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class ManagementBase(BaseModel):
    full_name_uz: str
    full_name_ru: str
    full_name_en: str
    position_uz: str
    position_ru: str
    position_en: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    reception_days_uz: Optional[str] = None
    reception_days_ru: Optional[str] = None
    reception_days_en: Optional[str] = None
    bio_uz: Optional[str] = None
    bio_ru: Optional[str] = None
    bio_en: Optional[str] = None
    display_order: Optional[int] = 0

class ManagementCreate(ManagementBase):
    pass

class ManagementUpdate(BaseModel):
    full_name_uz: Optional[str] = None
    full_name_ru: Optional[str] = None
    full_name_en: Optional[str] = None
    position_uz: Optional[str] = None
    position_ru: Optional[str] = None
    position_en: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    reception_days_uz: Optional[str] = None
    reception_days_ru: Optional[str] = None
    reception_days_en: Optional[str] = None
    bio_uz: Optional[str] = None
    bio_ru: Optional[str] = None
    bio_en: Optional[str] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None

class Management(ManagementBase):
    id: int
    photo_path: Optional[str] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class StructureBase(BaseModel):
    content_uz: str
    content_ru: str
    content_en: str

class StructureCreate(StructureBase):
    pass

class StructureUpdate(BaseModel):
    content_uz: Optional[str] = None
    content_ru: Optional[str] = None
    content_en: Optional[str] = None
    is_active: Optional[bool] = None

class Structure(StructureBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class StructuralDivisionBase(BaseModel):
    full_name_uz: str
    full_name_ru: str
    full_name_en: str
    position_uz: str
    position_ru: str
    position_en: str
    department_uz: str
    department_ru: str
    department_en: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    bio_uz: Optional[str] = None
    bio_ru: Optional[str] = None
    bio_en: Optional[str] = None
    display_order: Optional[int] = 0

class StructuralDivisionCreate(StructuralDivisionBase):
    pass

class StructuralDivisionUpdate(BaseModel):
    full_name_uz: Optional[str] = None
    full_name_ru: Optional[str] = None
    full_name_en: Optional[str] = None
    position_uz: Optional[str] = None
    position_ru: Optional[str] = None
    position_en: Optional[str] = None
    department_uz: Optional[str] = None
    department_ru: Optional[str] = None
    department_en: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    bio_uz: Optional[str] = None
    bio_ru: Optional[str] = None
    bio_en: Optional[str] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None

class StructuralDivision(StructuralDivisionBase):
    id: int
    photo_path: Optional[str] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class VacancyBase(BaseModel):
    position_uz: str
    position_ru: str
    position_en: str
    department_uz: str
    department_ru: str
    department_en: str
    requirements_uz: str
    requirements_ru: str
    requirements_en: str
    vacancy_status_uz: str
    vacancy_status_ru: str
    vacancy_status_en: str
    salary_range: Optional[str] = None
    deadline: Optional[datetime] = None

class VacancyCreate(VacancyBase):
    pass

class VacancyUpdate(BaseModel):
    position_uz: Optional[str] = None
    position_ru: Optional[str] = None
    position_en: Optional[str] = None
    department_uz: Optional[str] = None
    department_ru: Optional[str] = None
    department_en: Optional[str] = None
    requirements_uz: Optional[str] = None
    requirements_ru: Optional[str] = None
    requirements_en: Optional[str] = None
    vacancy_status_uz: Optional[str] = None
    vacancy_status_ru: Optional[str] = None
    vacancy_status_en: Optional[str] = None
    salary_range: Optional[str] = None
    deadline: Optional[datetime] = None
    is_active: Optional[bool] = None

class Vacancy(VacancyBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
