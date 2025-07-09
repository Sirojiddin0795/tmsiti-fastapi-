from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db.models.activity import ManagementSystem, Laboratory
from app.schemas.activity import (
    ManagementSystem as ManagementSystemSchema, ManagementSystemCreate, ManagementSystemUpdate,
    Laboratory as LaboratorySchema, LaboratoryCreate, LaboratoryUpdate
)
from app.api.v1.auth import get_moderator_user
from app.services.utils import save_uploaded_file
import os

router = APIRouter()

# Management System endpoints
@router.get("/management-system", response_model=ManagementSystemSchema)
async def get_management_system(db: Session = Depends(get_db)):
    """Get management system certification information"""
    system = db.query(ManagementSystem).filter(ManagementSystem.is_active == True).first()
    if not system:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Management system information not found"
        )
    return system

@router.post("/management-system", response_model=ManagementSystemSchema)
async def create_management_system(
    system_data: ManagementSystemCreate,
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Create or update management system information (moderator/admin only)"""
    existing_system = db.query(ManagementSystem).filter(ManagementSystem.is_active == True).first()
    if existing_system:
        # Update existing
        update_data = system_data.dict()
        for field, value in update_data.items():
            setattr(existing_system, field, value)
        db.commit()
        db.refresh(existing_system)
        return existing_system
    else:
        # Create new
        db_system = ManagementSystem(**system_data.dict())
        db.add(db_system)
        db.commit()
        db.refresh(db_system)
        return db_system

@router.put("/management-system/{system_id}", response_model=ManagementSystemSchema)
async def update_management_system(
    system_id: int,
    system_update: ManagementSystemUpdate,
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Update management system (moderator/admin only)"""
    system = db.query(ManagementSystem).filter(ManagementSystem.id == system_id).first()
    if not system:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Management system not found"
        )
    
    update_data = system_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(system, field, value)
    
    db.commit()
    db.refresh(system)
    return system

@router.post("/management-system/upload-pdf")
async def upload_management_system_pdf(
    file: UploadFile = File(...),
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Upload PDF for management system"""
    system = db.query(ManagementSystem).filter(ManagementSystem.is_active == True).first()
    if not system:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Management system not found"
        )
    
    # Save file
    file_path = await save_uploaded_file(file, "management_system", ["document"])
    
    # Remove old PDF if exists
    if system.pdf_path and os.path.exists(system.pdf_path):
        os.remove(system.pdf_path)
    
    system.pdf_path = file_path
    db.commit()
    
    return {"message": "PDF uploaded successfully", "file_path": file_path}

# Laboratory endpoints
@router.get("/laboratory", response_model=LaboratorySchema)
async def get_laboratory(db: Session = Depends(get_db)):
    """Get laboratory information"""
    lab = db.query(Laboratory).filter(Laboratory.is_active == True).first()
    if not lab:
        # Return default laboratory info if not found
        return {
            "id": 0,
            "ksl_link": "https://ksl.uz",
            "description_uz": "Laboratoriya haqida ma'lumot topilmadi",
            "description_ru": "Информация о лаборатории не найдена",
            "description_en": "Laboratory information not found",
            "is_active": True,
            "created_at": "2024-01-01T00:00:00"
        }
    return lab

@router.post("/laboratory", response_model=LaboratorySchema)
async def create_laboratory(
    lab_data: LaboratoryCreate,
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Create or update laboratory information (moderator/admin only)"""
    existing_lab = db.query(Laboratory).filter(Laboratory.is_active == True).first()
    if existing_lab:
        # Update existing
        update_data = lab_data.dict()
        for field, value in update_data.items():
            if value is not None:  # Only update non-None values
                setattr(existing_lab, field, value)
        db.commit()
        db.refresh(existing_lab)
        return existing_lab
    else:
        # Create new
        db_lab = Laboratory(**lab_data.dict())
        db.add(db_lab)
        db.commit()
        db.refresh(db_lab)
        return db_lab

@router.put("/laboratory/{lab_id}", response_model=LaboratorySchema)
async def update_laboratory(
    lab_id: int,
    lab_update: LaboratoryUpdate,
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Update laboratory (moderator/admin only)"""
    lab = db.query(Laboratory).filter(Laboratory.id == lab_id).first()
    if not lab:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Laboratory not found"
        )
    
    update_data = lab_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(lab, field, value)
    
    db.commit()
    db.refresh(lab)
    return lab
