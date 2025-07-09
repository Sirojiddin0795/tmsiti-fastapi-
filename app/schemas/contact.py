from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ContactBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    subject: Optional[str] = None
    message: str

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    is_read: Optional[bool] = None
    is_replied: Optional[bool] = None
    admin_response: Optional[str] = None

class Contact(ContactBase):
    id: int
    is_read: bool
    is_replied: bool
    admin_response: Optional[str] = None
    responded_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class AntiCorruptionBase(BaseModel):
    content_uz: str
    content_ru: str
    content_en: str
    contact_phone: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    hotline_uz: Optional[str] = None
    hotline_ru: Optional[str] = None
    hotline_en: Optional[str] = None

class AntiCorruptionCreate(AntiCorruptionBase):
    pass

class AntiCorruptionUpdate(BaseModel):
    content_uz: Optional[str] = None
    content_ru: Optional[str] = None
    content_en: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    hotline_uz: Optional[str] = None
    hotline_ru: Optional[str] = None
    hotline_en: Optional[str] = None
    is_active: Optional[bool] = None

class AntiCorruption(AntiCorruptionBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
