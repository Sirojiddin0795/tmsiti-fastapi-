from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.db.models.user import User
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token
from datetime import datetime

class AuthService:
    """Authentication service for handling user authentication operations"""
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        """
        Authenticate user with username and password
        
        Args:
            db: Database session
            username: Username or email
            password: Plain text password
            
        Returns:
            User object if authentication successful, None otherwise
        """
        # Try to find user by username or email
        user = db.query(User).filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        if not user.is_active:
            return None
        
        # Update last login time
        user.last_login = datetime.utcnow()
        db.commit()
        
        return user
    
    @staticmethod
    def create_user_tokens(user: User) -> Dict[str, str]:
        """
        Create access and refresh tokens for user
        
        Args:
            user: User object
            
        Returns:
            Dictionary containing access_token, refresh_token, and token_type
        """
        access_token = create_access_token(subject=user.id)
        refresh_token = create_refresh_token(subject=user.id)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
    @staticmethod
    def create_user(
        db: Session,
        username: str,
        email: str,
        full_name: str,
        password: str,
        phone: Optional[str] = None,
        bio: Optional[str] = None,
        is_admin: bool = False,
        is_moderator: bool = False
    ) -> User:
        """
        Create a new user
        
        Args:
            db: Database session
            username: Unique username
            email: Unique email address
            full_name: User's full name
            password: Plain text password
            phone: Optional phone number
            bio: Optional biography
            is_admin: Whether user is admin
            is_moderator: Whether user is moderator
            
        Returns:
            Created User object
        """
        hashed_password = get_password_hash(password)
        
        db_user = User(
            username=username,
            email=email,
            full_name=full_name,
            hashed_password=hashed_password,
            phone=phone,
            bio=bio,
            is_admin=is_admin,
            is_moderator=is_moderator
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
    
    @staticmethod
    def update_user_password(db: Session, user: User, new_password: str) -> bool:
        """
        Update user password
        
        Args:
            db: Database session
            user: User object
            new_password: New plain text password
            
        Returns:
            True if successful
        """
        user.hashed_password = get_password_hash(new_password)
        db.commit()
        return True
    
    @staticmethod
    def verify_user_permissions(user: User, required_role: str) -> bool:
        """
        Verify if user has required permissions
        
        Args:
            user: User object
            required_role: Required role ('admin', 'moderator', 'user')
            
        Returns:
            True if user has required permissions
        """
        if not user.is_active:
            return False
        
        if required_role == "admin":
            return user.is_admin
        elif required_role == "moderator":
            return user.is_admin or user.is_moderator
        elif required_role == "user":
            return True
        
        return False
    
    @staticmethod
    def deactivate_user(db: Session, user: User) -> bool:
        """
        Deactivate user account
        
        Args:
            db: Database session
            user: User object
            
        Returns:
            True if successful
        """
        user.is_active = False
        db.commit()
        return True
    
    @staticmethod
    def activate_user(db: Session, user: User) -> bool:
        """
        Activate user account
        
        Args:
            db: Database session
            user: User object
            
        Returns:
            True if successful
        """
        user.is_active = True
        db.commit()
        return True
    
    @staticmethod
    def promote_to_moderator(db: Session, user: User) -> bool:
        """
        Promote user to moderator
        
        Args:
            db: Database session
            user: User object
            
        Returns:
            True if successful
        """
        user.is_moderator = True
        db.commit()
        return True
    
    @staticmethod
    def demote_from_moderator(db: Session, user: User) -> bool:
        """
        Demote user from moderator
        
        Args:
            db: Database session
            user: User object
            
        Returns:
            True if successful
        """
        user.is_moderator = False
        db.commit()
        return True
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """
        Get user by ID
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            User object if found, None otherwise
        """
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """
        Get user by username
        
        Args:
            db: Database session
            username: Username
            
        Returns:
            User object if found, None otherwise
        """
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """
        Get user by email
        
        Args:
            db: Database session
            email: Email address
            
        Returns:
            User object if found, None otherwise
        """
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def is_username_available(db: Session, username: str, exclude_user_id: Optional[int] = None) -> bool:
        """
        Check if username is available
        
        Args:
            db: Database session
            username: Username to check
            exclude_user_id: User ID to exclude from check (for updates)
            
        Returns:
            True if username is available
        """
        query = db.query(User).filter(User.username == username)
        if exclude_user_id:
            query = query.filter(User.id != exclude_user_id)
        
        return query.first() is None
    
    @staticmethod
    def is_email_available(db: Session, email: str, exclude_user_id: Optional[int] = None) -> bool:
        """
        Check if email is available
        
        Args:
            db: Database session
            email: Email to check
            exclude_user_id: User ID to exclude from check (for updates)
            
        Returns:
            True if email is available
        """
        query = db.query(User).filter(User.email == email)
        if exclude_user_id:
            query = query.filter(User.id != exclude_user_id)
        
        return query.first() is None
