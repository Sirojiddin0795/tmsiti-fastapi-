from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NewsBase(BaseModel):
    title_uz: str
    title_ru: str
    title_en: str
    content_uz: str
    content_ru: str
    content_en: str
    is_featured: Optional[bool] = False

class NewsCreate(NewsBase):
    pass

class NewsUpdate(BaseModel):
    title_uz: Optional[str] = None
    title_ru: Optional[str] = None
    title_en: Optional[str] = None
    content_uz: Optional[str] = None
    content_ru: Optional[str] = None
    content_en: Optional[str] = None
    is_featured: Optional[bool] = None
    is_active: Optional[bool] = None

class News(NewsBase):
    id: int
    image_path: Optional[str] = None
    video_path: Optional[str] = None
    is_active: bool
    published_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

class AnnouncementBase(BaseModel):
    title_uz: str
    title_ru: str
    title_en: str
    content_uz: str
    content_ru: str
    content_en: str

class AnnouncementCreate(AnnouncementBase):
    pass

class AnnouncementUpdate(BaseModel):
    title_uz: Optional[str] = None
    title_ru: Optional[str] = None
    title_en: Optional[str] = None
    content_uz: Optional[str] = None
    content_ru: Optional[str] = None
    content_en: Optional[str] = None
    is_active: Optional[bool] = None

class Announcement(AnnouncementBase):
    id: int
    image_path: Optional[str] = None
    video_path: Optional[str] = None
    is_active: bool
    published_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True
