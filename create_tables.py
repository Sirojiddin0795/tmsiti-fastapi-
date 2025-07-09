#!/usr/bin/env python3
"""
Database initialization script for TMSITI backend
Creates all tables and sets up initial admin user
"""

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import Base, engine
from app.db.models.user import User
from app.core.security import get_password_hash
from app.core.config import settings

def create_tables():
    """Create all database tables"""
    try:
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables created successfully!")
        return True
    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        return False

def create_admin_user():
    """Create initial admin user if not exists"""
    try:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Check if admin user already exists
        admin_user = db.query(User).filter(User.username == "admin").first()
        
        if admin_user:
            print("✓ Admin user already exists")
            db.close()
            return True
        
        # Create admin user
        print("Creating admin user...")
        admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
        
        admin_user = User(
            username="admin",
            email="admin@tmsiti.uz",
            full_name="TMSITI Administrator",
            hashed_password=get_password_hash(admin_password),
            is_admin=True,
            is_active=True,
            phone="+998712345678",
            bio="System Administrator"
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print(f"✓ Admin user created successfully!")
        print(f"  Username: admin")
        print(f"  Email: admin@tmsiti.uz")
        print(f"  Password: {admin_password}")
        print("  ⚠️ Please change the default password after first login!")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"✗ Error creating admin user: {e}")
        return False

def create_sample_data():
    """Create sample data for testing (optional)"""
    try:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        print("Creating sample data...")
        
        # Sample content will be added here if needed
        # For now, we'll just create the structure
        
        db.commit()
        print("✓ Sample data created successfully!")
        db.close()
        return True
        
    except Exception as e:
        print(f"✗ Error creating sample data: {e}")
        return False

def setup_directories():
    """Create necessary directories for file uploads"""
    try:
        print("Setting up directories...")
        
        directories = [
            "static",
            "static/uploads",
            "static/uploads/news",
            "static/uploads/announcements",
            "static/uploads/management",
            "static/uploads/structural_divisions",
            "static/uploads/standards",
            "static/uploads/building_regulations",
            "static/uploads/references",
            "static/uploads/about",
            "static/uploads/management_system",
            "static/default"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        print("✓ Directories created successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Error creating directories: {e}")
        return False

def main():
    """Main initialization function"""
    print("TMSITI Database Initialization")
    print("=" * 50)
    
    # Check database connection
    try:
        engine.connect()
        print("✓ Database connection successful!")
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False
    
    success = True
    
    # Setup directories
    if not setup_directories():
        success = False
    
    # Create tables
    if not create_tables():
        success = False
    
    # Create admin user
    if not create_admin_user():
        success = False
    
    # Create sample data (optional)
    if "--with-sample-data" in sys.argv:
        if not create_sample_data():
            success = False
    
    print("=" * 50)
    if success:
        print("✓ Database initialization completed successfully!")
        print("\nNext steps:")
        print("1. Start the FastAPI server: uvicorn app.main:app --host 0.0.0.0 --port 8000")
        print("2. Access the API documentation: http://localhost:8000/docs")
        print("3. Login with admin credentials and change the default password")
    else:
        print("✗ Database initialization completed with errors!")
        return False
    
    return True

if __name__ == "__main__":
    if main():
        sys.exit(0)
    else:
        sys.exit(1)
