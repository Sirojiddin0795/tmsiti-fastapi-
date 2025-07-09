from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.db.models.institute import About, Management, Structure, StructuralDivision, Vacancy
from app.schemas.institute import (
    About as AboutSchema, AboutCreate, AboutUpdate,
    Management as ManagementSchema, ManagementCreate, ManagementUpdate,
    Structure as StructureSchema, StructureCreate, StructureUpdate,
    StructuralDivision as StructuralDivisionSchema, StructuralDivisionCreate, StructuralDivisionUpdate,
    Vacancy as VacancySchema, VacancyCreate, VacancyUpdate
)
from app.api.v1.auth import get_moderator_user
from app.services.utils import save_uploaded_file
import os

router = APIRouter()

# About endpoints
@router.get("/about", response_model=AboutSchema)
async def get_about(db: Session = Depends(get_db)):
    """Get institute about information"""
    about = db.query(About).filter(About.is_active == True).first()
    if not about:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="About information not found"
        )
    return about

@router.post("/about", response_model=AboutSchema)
async def create_about(
    about_data: AboutCreate,
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Create or update about information (moderator/admin only)"""
    # Check if about already exists
    existing_about = db.query(About).filter(About.is_active == True).first()
    if existing_about:
        # Update existing
        update_data = about_data.dict()
        for field, value in update_data.items():
            setattr(existing_about, field, value)
        db.commit()
        db.refresh(existing_about)
        return existing_about
    else:
        # Create new
        db_about = About(**about_data.dict())
        db.add(db_about)
        db.commit()
        db.refresh(db_about)
        return db_about

@router.post("/about/upload-certificate")
async def upload_about_certificate(
    file: UploadFile = File(...),
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Upload certificate PDF for about section"""
    about = db.query(About).filter(About.is_active == True).first()
    if not about:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="About information not found"
        )
    
    # Save file
    file_path = await save_uploaded_file(file, "about", ["document"])
    
    # Remove old certificate if exists
    if about.certificate_pdf_path and os.path.exists(about.certificate_pdf_path):
        os.remove(about.certificate_pdf_path)
    
    about.certificate_pdf_path = file_path
    db.commit()
    
    return {"message": "Certificate uploaded successfully", "file_path": file_path}

# Management endpoints
@router.get("/management", response_model=List[ManagementSchema])
async def get_management(
    request: Request,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get management list"""
    query = db.query(Management).filter(Management.is_active == True)
    
    if search:
        language = getattr(request.state, 'language', 'uz')
        if language == 'uz':
            query = query.filter(
                Management.full_name_uz.contains(search) | 
                Management.position_uz.contains(search)
            )
        elif language == 'ru':
            query = query.filter(
                Management.full_name_ru.contains(search) | 
                Management.position_ru.contains(search)
            )
        elif language == 'en':
            query = query.filter(
                Management.full_name_en.contains(search) | 
                Management.position_en.contains(search)
            )
    
    management = query.order_by(Management.display_order.asc()).all()
    return management

@router.get("/management/{management_id}", response_model=ManagementSchema)
async def get_management_member(management_id: int, db: Session = Depends(get_db)):
    """Get single management member"""
    member = db.query(Management).filter(
        Management.id == management_id, 
        Management.is_active == True
    ).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Management member not found"
        )
    return member

@router.post("/management", response_model=ManagementSchema)
async def create_management_member(
    member_data: ManagementCreate,
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Create new management member (moderator/admin only)"""
    db_member = Management(**member_data.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

@router.put("/management/{management_id}", response_model=ManagementSchema)
async def update_management_member(
    management_id: int,
    member_update: ManagementUpdate,
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Update management member (moderator/admin only)"""
    member = db.query(Management).filter(Management.id == management_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Management member not found"
        )
    
    update_data = member_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(member, field, value)
    
    db.commit()
    db.refresh(member)
    return member

@router.post("/management/{management_id}/upload-photo")
async def upload_management_photo(
    management_id: int,
    file: UploadFile = File(...),
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Upload photo for management member"""
    member = db.query(Management).filter(Management.id == management_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Management member not found"
        )
    
    # Save file
    file_path = await save_uploaded_file(file, "management", ["image"])
    
    # Remove old photo if exists
    if member.photo_path and os.path.exists(member.photo_path):
        os.remove(member.photo_path)
    
    member.photo_path = file_path
    db.commit()
    
    return {"message": "Photo uploaded successfully", "file_path": file_path}

# Structure endpoints
@router.get("/structure", response_model=StructureSchema)
async def get_structure(db: Session = Depends(get_db)):
    """Get organizational structure"""
    structure = db.query(Structure).filter(Structure.is_active == True).first()
    if not structure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Structure information not found"
        )
    return structure

@router.post("/structure", response_model=StructureSchema)
async def create_structure(
    structure_data: StructureCreate,
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Create or update structure (moderator/admin only)"""
    existing_structure = db.query(Structure).filter(Structure.is_active == True).first()
    if existing_structure:
        # Update existing
        update_data = structure_data.dict()
        for field, value in update_data.items():
            setattr(existing_structure, field, value)
        db.commit()
        db.refresh(existing_structure)
        return existing_structure
    else:
        # Create new
        db_structure = Structure(**structure_data.dict())
        db.add(db_structure)
        db.commit()
        db.refresh(db_structure)
        return db_structure

# Structural Divisions endpoints
@router.get("/structural-divisions", response_model=List[StructuralDivisionSchema])
async def get_structural_divisions(
    request: Request,
    search: Optional[str] = None,
    department: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get structural divisions list"""
    query = db.query(StructuralDivision).filter(StructuralDivision.is_active == True)
    
    if search:
        language = getattr(request.state, 'language', 'uz')
        if language == 'uz':
            query = query.filter(
                StructuralDivision.full_name_uz.contains(search) | 
                StructuralDivision.position_uz.contains(search) |
                StructuralDivision.department_uz.contains(search)
            )
        elif language == 'ru':
            query = query.filter(
                StructuralDivision.full_name_ru.contains(search) | 
                StructuralDivision.position_ru.contains(search) |
                StructuralDivision.department_ru.contains(search)
            )
        elif language == 'en':
            query = query.filter(
                StructuralDivision.full_name_en.contains(search) | 
                StructuralDivision.position_en.contains(search) |
                StructuralDivision.department_en.contains(search)
            )
    
    if department:
        language = getattr(request.state, 'language', 'uz')
        if language == 'uz':
            query = query.filter(StructuralDivision.department_uz.contains(department))
        elif language == 'ru':
            query = query.filter(StructuralDivision.department_ru.contains(department))
        elif language == 'en':
            query = query.filter(StructuralDivision.department_en.contains(department))
    
    divisions = query.order_by(StructuralDivision.display_order.asc()).all()
    return divisions

@router.post("/structural-divisions", response_model=StructuralDivisionSchema)
async def create_structural_division(
    division_data: StructuralDivisionCreate,
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Create new structural division member (moderator/admin only)"""
    db_division = StructuralDivision(**division_data.dict())
    db.add(db_division)
    db.commit()
    db.refresh(db_division)
    return db_division

# Vacancies endpoints
@router.get("/vacancies", response_model=List[VacancySchema])
async def get_vacancies(
    request: Request,
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    department: Optional[str] = None,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """Get vacancies list"""
    query = db.query(Vacancy)
    
    if active_only:
        query = query.filter(Vacancy.is_active == True)
    
    if search:
        language = getattr(request.state, 'language', 'uz')
        if language == 'uz':
            query = query.filter(
                Vacancy.position_uz.contains(search) | 
                Vacancy.department_uz.contains(search)
            )
        elif language == 'ru':
            query = query.filter(
                Vacancy.position_ru.contains(search) | 
                Vacancy.department_ru.contains(search)
            )
        elif language == 'en':
            query = query.filter(
                Vacancy.position_en.contains(search) | 
                Vacancy.department_en.contains(search)
            )
    
    if department:
        language = getattr(request.state, 'language', 'uz')
        if language == 'uz':
            query = query.filter(Vacancy.department_uz.contains(department))
        elif language == 'ru':
            query = query.filter(Vacancy.department_ru.contains(department))
        elif language == 'en':
            query = query.filter(Vacancy.department_en.contains(department))
    
    vacancies = query.order_by(Vacancy.created_at.desc()).offset(skip).limit(limit).all()
    return vacancies

@router.post("/vacancies", response_model=VacancySchema)
async def create_vacancy(
    vacancy_data: VacancyCreate,
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Create new vacancy (moderator/admin only)"""
    db_vacancy = Vacancy(**vacancy_data.dict())
    db.add(db_vacancy)
    db.commit()
    db.refresh(db_vacancy)
    return db_vacancy

@router.put("/vacancies/{vacancy_id}", response_model=VacancySchema)
async def update_vacancy(
    vacancy_id: int,
    vacancy_update: VacancyUpdate,
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Update vacancy (moderator/admin only)"""
    vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
    if not vacancy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vacancy not found"
        )
    
    update_data = vacancy_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(vacancy, field, value)
    
    db.commit()
    db.refresh(vacancy)
    return vacancy
