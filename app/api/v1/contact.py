from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.db.models.contact import Contact, AntiCorruption
from app.schemas.contact import (
    Contact as ContactSchema, ContactCreate, ContactUpdate,
    AntiCorruption as AntiCorruptionSchema, AntiCorruptionCreate, AntiCorruptionUpdate
)
from app.api.v1.auth import get_moderator_user
from datetime import datetime

router = APIRouter()

# Contact/Inquiry endpoints
@router.post("/", response_model=ContactSchema)
async def create_contact(
    contact_data: ContactCreate,
    db: Session = Depends(get_db)
):
    """Create new contact inquiry (public endpoint)"""
    db_contact = Contact(**contact_data.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.get("/", response_model=List[ContactSchema])
async def get_contacts(
    skip: int = 0,
    limit: int = 20,
    unread_only: bool = False,
    search: Optional[str] = None,
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Get contact inquiries list (moderator/admin only)"""
    query = db.query(Contact)
    
    if unread_only:
        query = query.filter(Contact.is_read == False)
    
    if search:
        query = query.filter(
            Contact.full_name.contains(search) |
            Contact.email.contains(search) |
            Contact.subject.contains(search) |
            Contact.message.contains(search)
        )
    
    contacts = query.order_by(Contact.created_at.desc()).offset(skip).limit(limit).all()
    return contacts

@router.get("/{contact_id}", response_model=ContactSchema)
async def get_contact(
    contact_id: int,
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Get single contact inquiry (moderator/admin only)"""
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    
    # Mark as read when viewed
    if not contact.is_read:
        contact.is_read = True
        db.commit()
    
    return contact

@router.put("/{contact_id}", response_model=ContactSchema)
async def update_contact(
    contact_id: int,
    contact_update: ContactUpdate,
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Update contact inquiry (moderator/admin only)"""
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    
    update_data = contact_update.dict(exclude_unset=True)
    
    # If admin response is provided, mark as replied and set timestamp
    if "admin_response" in update_data and update_data["admin_response"]:
        contact.admin_response = update_data["admin_response"]
        contact.is_replied = True
        contact.responded_at = datetime.utcnow()
    
    # Update other fields
    for field, value in update_data.items():
        if field != "admin_response":  # Already handled above
            setattr(contact, field, value)
    
    db.commit()
    db.refresh(contact)
    return contact

@router.delete("/{contact_id}")
async def delete_contact(
    contact_id: int,
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Delete contact inquiry (moderator/admin only)"""
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    
    db.delete(contact)
    db.commit()
    
    return {"message": "Contact deleted successfully"}

# Anti-corruption endpoints
@router.get("/anti-corruption", response_model=AntiCorruptionSchema)
async def get_anti_corruption(db: Session = Depends(get_db)):
    """Get anti-corruption information"""
    anti_corruption = db.query(AntiCorruption).filter(AntiCorruption.is_active == True).first()
    if not anti_corruption:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anti-corruption information not found"
        )
    return anti_corruption

@router.post("/anti-corruption", response_model=AntiCorruptionSchema)
async def create_anti_corruption(
    anti_corruption_data: AntiCorruptionCreate,
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Create or update anti-corruption information (moderator/admin only)"""
    existing_anti_corruption = db.query(AntiCorruption).filter(AntiCorruption.is_active == True).first()
    if existing_anti_corruption:
        # Update existing
        update_data = anti_corruption_data.dict()
        for field, value in update_data.items():
            setattr(existing_anti_corruption, field, value)
        db.commit()
        db.refresh(existing_anti_corruption)
        return existing_anti_corruption
    else:
        # Create new
        db_anti_corruption = AntiCorruption(**anti_corruption_data.dict())
        db.add(db_anti_corruption)
        db.commit()
        db.refresh(db_anti_corruption)
        return db_anti_corruption

@router.put("/anti-corruption/{anti_corruption_id}", response_model=AntiCorruptionSchema)
async def update_anti_corruption(
    anti_corruption_id: int,
    anti_corruption_update: AntiCorruptionUpdate,
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Update anti-corruption information (moderator/admin only)"""
    anti_corruption = db.query(AntiCorruption).filter(AntiCorruption.id == anti_corruption_id).first()
    if not anti_corruption:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anti-corruption information not found"
        )
    
    update_data = anti_corruption_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(anti_corruption, field, value)
    
    db.commit()
    db.refresh(anti_corruption)
    return anti_corruption

# Statistics endpoint for admin
@router.get("/stats")
async def get_contact_stats(
    current_user = Depends(get_moderator_user),
    db: Session = Depends(get_db)
):
    """Get contact statistics (moderator/admin only)"""
    total_contacts = db.query(Contact).count()
    unread_contacts = db.query(Contact).filter(Contact.is_read == False).count()
    replied_contacts = db.query(Contact).filter(Contact.is_replied == True).count()
    
    return {
        "total_contacts": total_contacts,
        "unread_contacts": unread_contacts,
        "replied_contacts": replied_contacts,
        "unreplied_contacts": total_contacts - replied_contacts
    }
