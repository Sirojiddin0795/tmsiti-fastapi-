from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.db.models.regulations import Law, UrbanNorm, Standard, BuildingRegulation, SmetaResourceNorm, Reference
from app.schemas.regulations import (
    Law as LawSchema, LawCreate, LawUpdate,
    UrbanNorm as UrbanNormSchema, UrbanNormCreate, UrbanNormUpdate,
    Standard as StandardSchema, StandardCreate, StandardUpdate,
    BuildingRegulation as BuildingRegulationSchema, BuildingRegulationCreate, BuildingRegulationUpdate,
    SmetaResourceNorm as SmetaResourceNormSchema, SmetaResourceNormCreate, SmetaResourceNormUpdate,
    Reference as ReferenceSchema, ReferenceCreate, ReferenceUpdate
)
from app.api.v1.auth import get_moderator_user
from app.services.utils import save_uploaded_file
import os

router = APIRouter()

# Laws endpoints
@router.get("/laws", response_model=List[LawSchema])
async def get_laws(
    request: Request,
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get laws list with pagination and search"""
    query = db.query(Law).filter(Law.is_active == True)
    
    if search:
        language = getattr(request.state, 'language', 'uz')
        if language == 'uz':
            query = query.filter(Law.name_uz.contains(search) | Law.authority_uz.contains(search))
        elif language == 'ru':
            query = query.filter(Law.name_ru.contains(search) | Law.authority_ru.contains(search))
        elif language == 'en':
            query = query.filter(Law.name_en.contains(search) | Law.authority_en.contains(search))
    
    laws = query.order_by(Law.adoption_date.desc()).offset(skip).limit(limit).all()
    return laws

@router.get("/laws/{law_id}", response_model=LawSchema)
async def get_law(law_id: int, db: Session = Depends(get_db)):
    """Get single law"""
    law = db.query(Law).filter(Law.id == law_id, Law.is_active == True).first()
    if not law:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Law not found"
        )
    return law

@router.post("/laws", response_model=LawSchema)
async def create_law(
    law_data: LawCreate,
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Create new law (moderator/admin only)"""
    db_law = Law(**law_data.dict())
    db.add(db_law)
    db.commit()
    db.refresh(db_law)
    return db_law

@router.put("/laws/{law_id}", response_model=LawSchema)
async def update_law(
    law_id: int,
    law_update: LawUpdate,
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Update law (moderator/admin only)"""
    law = db.query(Law).filter(Law.id == law_id).first()
    if not law:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Law not found"
        )
    
    update_data = law_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(law, field, value)
    
    db.commit()
    db.refresh(law)
    return law

@router.delete("/laws/{law_id}")
async def delete_law(
    law_id: int,
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Delete law (moderator/admin only)"""
    law = db.query(Law).filter(Law.id == law_id).first()
    if not law:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Law not found"
        )
    
    db.delete(law)
    db.commit()
    return {"message": "Law deleted successfully"}

# Urban Norms endpoints
@router.get("/urban-norms", response_model=List[UrbanNormSchema])
async def get_urban_norms(
    request: Request,
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get urban norms list with pagination and search"""
    query = db.query(UrbanNorm).filter(UrbanNorm.is_active == True)
    
    if search:
        language = getattr(request.state, 'language', 'uz')
        if language == 'uz':
            query = query.filter(UrbanNorm.name_uz.contains(search) | UrbanNorm.document_code.contains(search))
        elif language == 'ru':
            query = query.filter(UrbanNorm.name_ru.contains(search) | UrbanNorm.document_code.contains(search))
        elif language == 'en':
            query = query.filter(UrbanNorm.name_en.contains(search) | UrbanNorm.document_code.contains(search))
    
    norms = query.order_by(UrbanNorm.created_at.desc()).offset(skip).limit(limit).all()
    return norms

@router.post("/urban-norms", response_model=UrbanNormSchema)
async def create_urban_norm(
    norm_data: UrbanNormCreate,
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Create new urban norm (moderator/admin only)"""
    db_norm = UrbanNorm(**norm_data.dict())
    db.add(db_norm)
    db.commit()
    db.refresh(db_norm)
    return db_norm

# Standards endpoints
@router.get("/standards", response_model=List[StandardSchema])
async def get_standards(
    request: Request,
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get standards list with pagination and search"""
    query = db.query(Standard).filter(Standard.is_active == True)
    
    if search:
        language = getattr(request.state, 'language', 'uz')
        if language == 'uz':
            query = query.filter(Standard.name_uz.contains(search))
        elif language == 'ru':
            query = query.filter(Standard.name_ru.contains(search))
        elif language == 'en':
            query = query.filter(Standard.name_en.contains(search))
    
    standards = query.order_by(Standard.created_at.desc()).offset(skip).limit(limit).all()
    return standards

@router.post("/standards", response_model=StandardSchema)
async def create_standard(
    standard_data: StandardCreate,
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Create new standard (moderator/admin only)"""
    db_standard = Standard(**standard_data.dict())
    db.add(db_standard)
    db.commit()
    db.refresh(db_standard)
    return db_standard

@router.post("/standards/{standard_id}/upload-pdf")
async def upload_standard_pdf(
    standard_id: int,
    file: UploadFile = File(...),
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Upload PDF for standard"""
    standard = db.query(Standard).filter(Standard.id == standard_id).first()
    if not standard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Standard not found"
        )
    
    # Save file
    file_path = await save_uploaded_file(file, "standards", ["document"])
    
    # Remove old PDF if exists
    if standard.pdf_path and os.path.exists(standard.pdf_path):
        os.remove(standard.pdf_path)
    
    standard.pdf_path = file_path
    db.commit()
    
    return {"message": "PDF uploaded successfully", "file_path": file_path}

# Building Regulations endpoints
@router.get("/building-regulations", response_model=List[BuildingRegulationSchema])
async def get_building_regulations(
    request: Request,
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get building regulations list with pagination and search"""
    query = db.query(BuildingRegulation).filter(BuildingRegulation.is_active == True)
    
    if search:
        language = getattr(request.state, 'language', 'uz')
        if language == 'uz':
            query = query.filter(
                BuildingRegulation.name_uz.contains(search) | 
                BuildingRegulation.document_number.contains(search)
            )
        elif language == 'ru':
            query = query.filter(
                BuildingRegulation.name_ru.contains(search) | 
                BuildingRegulation.document_number.contains(search)
            )
        elif language == 'en':
            query = query.filter(
                BuildingRegulation.name_en.contains(search) | 
                BuildingRegulation.document_number.contains(search)
            )
    
    regulations = query.order_by(BuildingRegulation.created_at.desc()).offset(skip).limit(limit).all()
    return regulations

@router.post("/building-regulations", response_model=BuildingRegulationSchema)
async def create_building_regulation(
    regulation_data: BuildingRegulationCreate,
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Create new building regulation (moderator/admin only)"""
    db_regulation = BuildingRegulation(**regulation_data.dict())
    db.add(db_regulation)
    db.commit()
    db.refresh(db_regulation)
    return db_regulation

# Smeta Resource Norms endpoints
@router.get("/smeta-resource-norms", response_model=List[SmetaResourceNormSchema])
async def get_smeta_resource_norms(
    request: Request,
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get smeta resource norms list with pagination and search"""
    query = db.query(SmetaResourceNorm).filter(SmetaResourceNorm.is_active == True)
    
    if search:
        language = getattr(request.state, 'language', 'uz')
        if language == 'uz':
            query = query.filter(
                SmetaResourceNorm.shnq_name_uz.contains(search) | 
                SmetaResourceNorm.document_number.contains(search)
            )
        elif language == 'ru':
            query = query.filter(
                SmetaResourceNorm.shnq_name_ru.contains(search) | 
                SmetaResourceNorm.document_number.contains(search)
            )
        elif language == 'en':
            query = query.filter(
                SmetaResourceNorm.shnq_name_en.contains(search) | 
                SmetaResourceNorm.document_number.contains(search)
            )
    
    norms = query.order_by(SmetaResourceNorm.created_at.desc()).offset(skip).limit(limit).all()
    return norms

@router.post("/smeta-resource-norms", response_model=SmetaResourceNormSchema)
async def create_smeta_resource_norm(
    norm_data: SmetaResourceNormCreate,
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Create new smeta resource norm (moderator/admin only)"""
    db_norm = SmetaResourceNorm(**norm_data.dict())
    db.add(db_norm)
    db.commit()
    db.refresh(db_norm)
    return db_norm

# References endpoints
@router.get("/references", response_model=List[ReferenceSchema])
async def get_references(
    request: Request,
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get references list with pagination and search"""
    query = db.query(Reference).filter(Reference.is_active == True)
    
    if search:
        language = getattr(request.state, 'language', 'uz')
        if language == 'uz':
            query = query.filter(
                Reference.name_uz.contains(search) | 
                Reference.reference_number.contains(search)
            )
        elif language == 'ru':
            query = query.filter(
                Reference.name_ru.contains(search) | 
                Reference.reference_number.contains(search)
            )
        elif language == 'en':
            query = query.filter(
                Reference.name_en.contains(search) | 
                Reference.reference_number.contains(search)
            )
    
    references = query.order_by(Reference.created_at.desc()).offset(skip).limit(limit).all()
    return references

@router.post("/references", response_model=ReferenceSchema)
async def create_reference(
    reference_data: ReferenceCreate,
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Create new reference (moderator/admin only)"""
    db_reference = Reference(**reference_data.dict())
    db.add(db_reference)
    db.commit()
    db.refresh(db_reference)
    return db_reference

@router.post("/references/{reference_id}/upload-pdf")
async def upload_reference_pdf(
    reference_id: int,
    file: UploadFile = File(...),
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Upload PDF for reference"""
    reference = db.query(Reference).filter(Reference.id == reference_id).first()
    if not reference:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reference not found"
        )
    
    # Save file
    file_path = await save_uploaded_file(file, "references", ["document"])
    
    # Remove old PDF if exists
    if reference.pdf_path and os.path.exists(reference.pdf_path):
        os.remove(reference.pdf_path)
    
    reference.pdf_path = file_path
    db.commit()
    
    return {"message": "PDF uploaded successfully", "file_path": file_path}
