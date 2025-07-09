from app.db.models.user import User
from app.db.models.news import News, Announcement
from app.db.models.regulations import Law, UrbanNorm, Standard, BuildingRegulation, SmetaResourceNorm, Reference
from app.db.models.institute import About, Management, Structure, StructuralDivision, Vacancy
from app.db.models.activity import ManagementSystem, Laboratory
from app.db.models.contact import Contact, AntiCorruption

__all__ = [
    "User",
    "News",
    "Announcement", 
    "Law",
    "UrbanNorm",
    "Standard",
    "BuildingRegulation",
    "SmetaResourceNorm",
    "Reference",
    "About",
    "Management",
    "Structure",
    "StructuralDivision",
    "Vacancy",
    "ManagementSystem",
    "Laboratory",
    "Contact",
    "AntiCorruption"
]
