from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.db.models.news import News, Announcement
from app.schemas.news import (
    News as NewsSchema, NewsCreate, NewsUpdate,
    Announcement as AnnouncementSchema, AnnouncementCreate, AnnouncementUpdate
)
from app.api.v1.auth import get_moderator_user
from app.services.utils import save_uploaded_file, get_localized_content
import os

router = APIRouter()

# News endpoints
@router.get("/", response_model=List[NewsSchema])
async def get_news(
    request: Request,
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    featured: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get news list with pagination and search"""
    query = db.query(News).filter(News.is_active == True)
    
    if featured is not None:
        query = query.filter(News.is_featured == featured)
    
    if search:
        language = getattr(request.state, 'language', 'uz')
        if language == 'uz':
            query = query.filter(News.title_uz.contains(search) | News.content_uz.contains(search))
        elif language == 'ru':
            query = query.filter(News.title_ru.contains(search) | News.content_ru.contains(search))
        elif language == 'en':
            query = query.filter(News.title_en.contains(search) | News.content_en.contains(search))
    
    news = query.order_by(News.published_date.desc()).offset(skip).limit(limit).all()
    return news

@router.get("/{news_id}", response_model=NewsSchema)
async def get_news_item(news_id: int, db: Session = Depends(get_db)):
    """Get single news item"""
    news = db.query(News).filter(News.id == news_id, News.is_active == True).first()
    if not news:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="News not found"
        )
    return news

@router.post("/", response_model=NewsSchema)
async def create_news(
    news_data: NewsCreate,
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Create new news (moderator/admin only)"""
    db_news = News(**news_data.dict())
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news

@router.put("/{news_id}", response_model=NewsSchema)
async def update_news(
    news_id: int,
    news_update: NewsUpdate,
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Update news (moderator/admin only)"""
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="News not found"
        )
    
    update_data = news_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(news, field, value)
    
    db.commit()
    db.refresh(news)
    return news

@router.post("/{news_id}/upload-image")
async def upload_news_image(
    news_id: int,
    file: UploadFile = File(...),
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Upload image for news"""
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="News not found"
        )
    
    # Save file
    file_path = await save_uploaded_file(file, "news", ["image"])
    
    # Remove old image if exists
    if news.image_path and os.path.exists(news.image_path):
        os.remove(news.image_path)
    
    news.image_path = file_path
    db.commit()
    
    return {"message": "Image uploaded successfully", "file_path": file_path}

@router.delete("/{news_id}")
async def delete_news(
    news_id: int,
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Delete news (moderator/admin only)"""
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="News not found"
        )
    
    # Remove files
    if news.image_path and os.path.exists(news.image_path):
        os.remove(news.image_path)
    if news.video_path and os.path.exists(news.video_path):
        os.remove(news.video_path)
    
    db.delete(news)
    db.commit()
    
    return {"message": "News deleted successfully"}

# Announcements endpoints
@router.get("/announcements/", response_model=List[AnnouncementSchema])
async def get_announcements(
    request: Request,
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get announcements list with pagination and search"""
    query = db.query(Announcement).filter(Announcement.is_active == True)
    
    if search:
        language = getattr(request.state, 'language', 'uz')
        if language == 'uz':
            query = query.filter(Announcement.title_uz.contains(search) | Announcement.content_uz.contains(search))
        elif language == 'ru':
            query = query.filter(Announcement.title_ru.contains(search) | Announcement.content_ru.contains(search))
        elif language == 'en':
            query = query.filter(Announcement.title_en.contains(search) | Announcement.content_en.contains(search))
    
    announcements = query.order_by(Announcement.published_date.desc()).offset(skip).limit(limit).all()
    return announcements

@router.get("/announcements/{announcement_id}", response_model=AnnouncementSchema)
async def get_announcement(announcement_id: int, db: Session = Depends(get_db)):
    """Get single announcement"""
    announcement = db.query(Announcement).filter(
        Announcement.id == announcement_id, 
        Announcement.is_active == True
    ).first()
    if not announcement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Announcement not found"
        )
    return announcement

@router.post("/announcements/", response_model=AnnouncementSchema)
async def create_announcement(
    announcement_data: AnnouncementCreate,
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Create new announcement (moderator/admin only)"""
    db_announcement = Announcement(**announcement_data.dict())
    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)
    return db_announcement

@router.put("/announcements/{announcement_id}", response_model=AnnouncementSchema)
async def update_announcement(
    announcement_id: int,
    announcement_update: AnnouncementUpdate,
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Update announcement (moderator/admin only)"""
    announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not announcement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Announcement not found"
        )
    
    update_data = announcement_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(announcement, field, value)
    
    db.commit()
    db.refresh(announcement)
    return announcement

@router.delete("/announcements/{announcement_id}")
async def delete_announcement(
    announcement_id: int,
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Delete announcement (moderator/admin only)"""
    announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not announcement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Announcement not found"
        )
    
    # Remove files
    if announcement.image_path and os.path.exists(announcement.image_path):
        os.remove(announcement.image_path)
    if announcement.video_path and os.path.exists(announcement.video_path):
        os.remove(announcement.video_path)
    
    db.delete(announcement)
    db.commit()
    
    return {"message": "Announcement deleted successfully"}
