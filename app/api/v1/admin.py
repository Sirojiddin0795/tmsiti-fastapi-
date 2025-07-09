from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from app.db.database import get_db
from app.db.models.user import User
from app.db.models.news import News, Announcement
from app.db.models.regulations import Law, UrbanNorm, Standard, BuildingRegulation, SmetaResourceNorm, Reference
from app.db.models.institute import About, Management, Structure, StructuralDivision, Vacancy
from app.db.models.activity import ManagementSystem, Laboratory
from app.db.models.contact import Contact, AntiCorruption
from app.api.v1.auth import get_admin_user, get_moderator_user
from app.core.config import settings

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard_stats(
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get dashboard statistics for admin panel"""
    
    # User statistics
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    admin_users = db.query(User).filter(User.is_admin == True).count()
    moderator_users = db.query(User).filter(User.is_moderator == True).count()
    
    # Content statistics
    total_news = db.query(News).count()
    active_news = db.query(News).filter(News.is_active == True).count()
    featured_news = db.query(News).filter(and_(News.is_active == True, News.is_featured == True)).count()
    
    total_announcements = db.query(Announcement).count()
    active_announcements = db.query(Announcement).filter(Announcement.is_active == True).count()
    
    # Regulations statistics
    total_laws = db.query(Law).count()
    total_standards = db.query(Standard).count()
    total_urban_norms = db.query(UrbanNorm).count()
    total_building_regulations = db.query(BuildingRegulation).count()
    
    # Contact statistics
    total_contacts = db.query(Contact).count()
    unread_contacts = db.query(Contact).filter(Contact.is_read == False).count()
    replied_contacts = db.query(Contact).filter(Contact.is_replied == True).count()
    
    # Recent activity (last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_news = db.query(News).filter(News.created_at >= week_ago).count()
    recent_contacts = db.query(Contact).filter(Contact.created_at >= week_ago).count()
    recent_users = db.query(User).filter(User.created_at >= week_ago).count()
    
    # Institute statistics
    total_management = db.query(Management).filter(Management.is_active == True).count()
    total_divisions = db.query(StructuralDivision).filter(StructuralDivision.is_active == True).count()
    total_vacancies = db.query(Vacancy).filter(Vacancy.is_active == True).count()
    
    return {
        "users": {
            "total": total_users,
            "active": active_users,
            "admins": admin_users,
            "moderators": moderator_users,
            "recent": recent_users
        },
        "content": {
            "news": {
                "total": total_news,
                "active": active_news,
                "featured": featured_news,
                "recent": recent_news
            },
            "announcements": {
                "total": total_announcements,
                "active": active_announcements
            }
        },
        "regulations": {
            "laws": total_laws,
            "standards": total_standards,
            "urban_norms": total_urban_norms,
            "building_regulations": total_building_regulations
        },
        "contacts": {
            "total": total_contacts,
            "unread": unread_contacts,
            "replied": replied_contacts,
            "recent": recent_contacts
        },
        "institute": {
            "management": total_management,
            "divisions": total_divisions,
            "vacancies": total_vacancies
        }
    }

@router.get("/users/analytics")
async def get_user_analytics(
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get user analytics for admin panel"""
    
    # User registration trends (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    # Daily registration counts
    daily_registrations = db.query(
        func.date(User.created_at).label('date'),
        func.count(User.id).label('count')
    ).filter(
        User.created_at >= thirty_days_ago
    ).group_by(
        func.date(User.created_at)
    ).order_by('date').all()
    
    # User role distribution
    role_distribution = {
        "regular_users": db.query(User).filter(
            and_(User.is_admin == False, User.is_moderator == False)
        ).count(),
        "moderators": db.query(User).filter(User.is_moderator == True).count(),
        "admins": db.query(User).filter(User.is_admin == True).count()
    }
    
    # User activity (users who logged in last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)
    active_users_week = db.query(User).filter(User.last_login >= week_ago).count()
    
    return {
        "daily_registrations": [
            {"date": str(item.date), "count": item.count}
            for item in daily_registrations
        ],
        "role_distribution": role_distribution,
        "active_users_last_week": active_users_week
    }

@router.get("/content/analytics")
async def get_content_analytics(
    current_user: User = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Get content analytics for admin/moderator panel"""
    
    # Content creation trends (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    # Daily content creation
    daily_news = db.query(
        func.date(News.created_at).label('date'),
        func.count(News.id).label('count')
    ).filter(
        News.created_at >= thirty_days_ago
    ).group_by(
        func.date(News.created_at)
    ).order_by('date').all()
    
    daily_announcements = db.query(
        func.date(Announcement.created_at).label('date'),
        func.count(Announcement.id).label('count')
    ).filter(
        Announcement.created_at >= thirty_days_ago
    ).group_by(
        func.date(Announcement.created_at)
    ).order_by('date').all()
    
    # Most recent content
    recent_news = db.query(News).order_by(News.created_at.desc()).limit(5).all()
    recent_announcements = db.query(Announcement).order_by(Announcement.created_at.desc()).limit(5).all()
    
    return {
        "daily_news": [
            {"date": str(item.date), "count": item.count}
            for item in daily_news
        ],
        "daily_announcements": [
            {"date": str(item.date), "count": item.count}
            for item in daily_announcements
        ],
        "recent_news": [
            {
                "id": news.id,
                "title_uz": news.title_uz,
                "title_ru": news.title_ru,
                "title_en": news.title_en,
                "created_at": news.created_at,
                "is_active": news.is_active,
                "is_featured": news.is_featured
            }
            for news in recent_news
        ],
        "recent_announcements": [
            {
                "id": announcement.id,
                "title_uz": announcement.title_uz,
                "title_ru": announcement.title_ru,
                "title_en": announcement.title_en,
                "created_at": announcement.created_at,
                "is_active": announcement.is_active
            }
            for announcement in recent_announcements
        ]
    }

@router.get("/system/info")
async def get_system_info(
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get system information for admin panel"""
    
    # Database statistics
    tables_info = {}
    
    # Count records in each main table
    model_counts = {
        "users": db.query(User).count(),
        "news": db.query(News).count(),
        "announcements": db.query(Announcement).count(),
        "laws": db.query(Law).count(),
        "urban_norms": db.query(UrbanNorm).count(),
        "standards": db.query(Standard).count(),
        "building_regulations": db.query(BuildingRegulation).count(),
        "smeta_resource_norms": db.query(SmetaResourceNorm).count(),
        "references": db.query(Reference).count(),
        "management": db.query(Management).count(),
        "structural_divisions": db.query(StructuralDivision).count(),
        "vacancies": db.query(Vacancy).count(),
        "contacts": db.query(Contact).count(),
        "management_systems": db.query(ManagementSystem).count(),
        "laboratories": db.query(Laboratory).count(),
        "anti_corruption": db.query(AntiCorruption).count()
    }
    
    # System settings
    system_settings = {
        "supported_languages": settings.supported_languages,
        "default_language": settings.default_language,
        "max_file_size": settings.max_file_size,
        "default_page_size": settings.default_page_size,
        "max_page_size": settings.max_page_size,
        "allowed_image_extensions": settings.allowed_image_extensions,
        "allowed_document_extensions": settings.allowed_document_extensions
    }
    
    return {
        "database_statistics": model_counts,
        "system_settings": system_settings,
        "server_time": datetime.utcnow().isoformat(),
        "api_version": "1.0.0"
    }

@router.get("/logs/recent")
async def get_recent_logs(
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=100)
):
    """Get recent activity logs for admin panel"""
    
    # This is a simplified log system - in production you might want to implement proper logging
    recent_activities = []
    
    # Recent user registrations
    recent_users = db.query(User).order_by(User.created_at.desc()).limit(10).all()
    for user in recent_users:
        recent_activities.append({
            "type": "user_registration",
            "description": f"New user registered: {user.username}",
            "timestamp": user.created_at,
            "user": user.username
        })
    
    # Recent content creation
    recent_news = db.query(News).order_by(News.created_at.desc()).limit(10).all()
    for news in recent_news:
        recent_activities.append({
            "type": "content_creation",
            "description": f"New news created: {news.title_uz[:50]}...",
            "timestamp": news.created_at,
            "content_type": "news"
        })
    
    # Recent contacts
    recent_contacts = db.query(Contact).order_by(Contact.created_at.desc()).limit(10).all()
    for contact in recent_contacts:
        recent_activities.append({
            "type": "contact_inquiry",
            "description": f"New contact from: {contact.full_name}",
            "timestamp": contact.created_at,
            "email": contact.email
        })
    
    # Sort by timestamp and limit
    recent_activities.sort(key=lambda x: x["timestamp"], reverse=True)
    recent_activities = recent_activities[:limit]
    
    return {
        "activities": recent_activities,
        "total_count": len(recent_activities)
    }

@router.post("/maintenance/cleanup")
async def cleanup_inactive_content(
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Cleanup inactive content and old records"""
    
    cleanup_results = {}
    
    # Mark very old unread contacts as read (older than 90 days)
    ninety_days_ago = datetime.utcnow() - timedelta(days=90)
    old_contacts = db.query(Contact).filter(
        and_(
            Contact.is_read == False,
            Contact.created_at < ninety_days_ago
        )
    ).update({"is_read": True})
    
    cleanup_results["old_contacts_marked_read"] = old_contacts
    
    # You can add more cleanup operations here
    # For example:
    # - Remove old inactive news
    # - Clean up orphaned files
    # - Archive old data
    
    db.commit()
    
    return {
        "message": "Cleanup completed successfully",
        "results": cleanup_results,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/search/global")
async def global_search(
    q: str = Query(..., min_length=2),
    current_user: User = Depends(get_moderator_user),
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=50)
):
    """Global search across all content types for admin panel"""
    
    results = {}
    
    # Search in news
    news_results = db.query(News).filter(
        or_(
            News.title_uz.contains(q),
            News.title_ru.contains(q),
            News.title_en.contains(q),
            News.content_uz.contains(q),
            News.content_ru.contains(q),
            News.content_en.contains(q)
        )
    ).limit(limit).all()
    
    results["news"] = [
        {
            "id": news.id,
            "title_uz": news.title_uz,
            "type": "news",
            "created_at": news.created_at,
            "is_active": news.is_active
        }
        for news in news_results
    ]
    
    # Search in users
    user_results = db.query(User).filter(
        or_(
            User.username.contains(q),
            User.full_name.contains(q),
            User.email.contains(q)
        )
    ).limit(limit).all()
    
    results["users"] = [
        {
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "type": "user",
            "is_active": user.is_active
        }
        for user in user_results
    ]
    
    # Search in laws
    law_results = db.query(Law).filter(
        or_(
            Law.name_uz.contains(q),
            Law.name_ru.contains(q),
            Law.name_en.contains(q),
            Law.order_number.contains(q)
        )
    ).limit(limit).all()
    
    results["laws"] = [
        {
            "id": law.id,
            "name_uz": law.name_uz,
            "order_number": law.order_number,
            "type": "law",
            "is_active": law.is_active
        }
        for law in law_results
    ]
    
    # Search in contacts
    contact_results = db.query(Contact).filter(
        or_(
            Contact.full_name.contains(q),
            Contact.email.contains(q),
            Contact.subject.contains(q),
            Contact.message.contains(q)
        )
    ).limit(limit).all()
    
    results["contacts"] = [
        {
            "id": contact.id,
            "full_name": contact.full_name,
            "email": contact.email,
            "type": "contact",
            "created_at": contact.created_at,
            "is_read": contact.is_read
        }
        for contact in contact_results
    ]
    
    # Calculate total results
    total_results = sum(len(results[key]) for key in results)
    
    return {
        "query": q,
        "total_results": total_results,
        "results": results
    }

@router.get("/export/data")
async def export_data(
    current_user: User = Depends(get_admin_user),
    table: str = Query(..., description="Table name to export"),
    format: str = Query("json", regex="^(json|csv)$"),
    db: Session = Depends(get_db)
):
    """Export data from specific tables for backup/analysis"""
    
    # This is a basic implementation - in production you might want to use
    # more sophisticated export tools and add proper file handling
    
    supported_tables = {
        "users": User,
        "news": News,
        "announcements": Announcement,
        "laws": Law,
        "contacts": Contact
    }
    
    if table not in supported_tables:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Table '{table}' not supported for export"
        )
    
    model = supported_tables[table]
    data = db.query(model).all()
    
    # Convert to dictionary format
    export_data = []
    for item in data:
        item_dict = {}
        for column in item.__table__.columns:
            value = getattr(item, column.name)
            if isinstance(value, datetime):
                value = value.isoformat()
            item_dict[column.name] = value
        export_data.append(item_dict)
    
    return {
        "table": table,
        "format": format,
        "record_count": len(export_data),
        "exported_at": datetime.utcnow().isoformat(),
        "data": export_data
    }
