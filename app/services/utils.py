import os
import uuid
import aiofiles
from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status, UploadFile
from PIL import Image
import mimetypes
from app.core.config import settings

async def save_uploaded_file(
    file: UploadFile, 
    folder: str, 
    allowed_types: List[str] = ["image", "document"]
) -> str:
    """
    Save uploaded file to storage
    
    Args:
        file: FastAPI UploadFile object
        folder: Subfolder in uploads directory
        allowed_types: List of allowed file types ("image", "document", "video")
        
    Returns:
        Relative path to saved file
        
    Raises:
        HTTPException: If file validation fails
    """
    
    # Validate file
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided"
        )
    
    # Check file size
    file_size = 0
    content = await file.read()
    file_size = len(content)
    
    if file_size > settings.max_file_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum allowed size of {settings.max_file_size} bytes"
        )
    
    # Reset file pointer
    await file.seek(0)
    
    # Get file extension
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    # Validate file type
    is_valid_file = False
    
    if "image" in allowed_types:
        if file_extension in settings.allowed_image_extensions:
            is_valid_file = True
    
    if "document" in allowed_types:
        if file_extension in settings.allowed_document_extensions:
            is_valid_file = True
    
    if not is_valid_file:
        allowed_extensions = []
        if "image" in allowed_types:
            allowed_extensions.extend(settings.allowed_image_extensions)
        if "document" in allowed_types:
            allowed_extensions.extend(settings.allowed_document_extensions)
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed extensions: {', '.join(allowed_extensions)}"
        )
    
    # Validate MIME type for additional security
    mime_type, _ = mimetypes.guess_type(file.filename)
    if mime_type:
        if "image" in allowed_types and mime_type.startswith("image/"):
            pass  # Valid image
        elif "document" in allowed_types and (
            mime_type.startswith("application/") or 
            mime_type.startswith("text/")
        ):
            pass  # Valid document
        else:
            # Additional validation for specific types
            allowed_mimes = []
            if "image" in allowed_types:
                allowed_mimes.extend(["image/jpeg", "image/png", "image/gif", "image/webp"])
            if "document" in allowed_types:
                allowed_mimes.extend(["application/pdf", "application/msword", 
                                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"])
            
            if mime_type not in allowed_mimes:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid file type. MIME type: {mime_type}"
                )
    
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    # Create directory if it doesn't exist
    upload_dir = f"static/uploads/{folder}"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Full file path
    file_path = f"{upload_dir}/{unique_filename}"
    
    # Save file
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}"
        )
    
    # Validate and resize image if it's an image file
    if "image" in allowed_types and file_extension in settings.allowed_image_extensions:
        try:
            await validate_and_resize_image(file_path)
        except Exception as e:
            # Remove the uploaded file if image processing fails
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid image file: {str(e)}"
            )
    
    return file_path

async def validate_and_resize_image(file_path: str, max_width: int = 1920, max_height: int = 1080):
    """
    Validate and resize image if necessary
    
    Args:
        file_path: Path to image file
        max_width: Maximum width in pixels
        max_height: Maximum height in pixels
    """
    try:
        with Image.open(file_path) as img:
            # Check if image is valid
            img.verify()
            
            # Reopen for processing (verify() closes the image)
            with Image.open(file_path) as img:
                # Convert to RGB if necessary (for PNG with transparency)
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                
                # Resize if image is too large
                if img.width > max_width or img.height > max_height:
                    # Calculate new size maintaining aspect ratio
                    ratio = min(max_width / img.width, max_height / img.height)
                    new_size = (int(img.width * ratio), int(img.height * ratio))
                    
                    # Resize image
                    img = img.resize(new_size, Image.Resampling.LANCZOS)
                    
                    # Save resized image
                    img.save(file_path, optimize=True, quality=85)
    
    except Exception as e:
        raise Exception(f"Image validation/processing failed: {str(e)}")

def delete_file(file_path: str) -> bool:
    """
    Delete file from storage
    
    Args:
        file_path: Path to file to delete
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception:
        return False

def get_localized_content(obj: Any, field_prefix: str, language: str) -> str:
    """
    Get localized content from object based on language
    
    Args:
        obj: Object containing multilingual fields
        field_prefix: Prefix of the field (e.g., "title", "content")
        language: Language code ("uz", "ru", "en")
        
    Returns:
        Localized content string
    """
    field_name = f"{field_prefix}_{language}"
    
    # Try to get the content in requested language
    content = getattr(obj, field_name, None)
    
    # If not found, try fallback languages
    if not content:
        fallback_languages = ["uz", "ru", "en"]
        for fallback_lang in fallback_languages:
            if fallback_lang != language:
                fallback_field = f"{field_prefix}_{fallback_lang}"
                content = getattr(obj, fallback_field, None)
                if content:
                    break
    
    return content or ""

def get_file_url(file_path: Optional[str], request_base_url: str = "") -> Optional[str]:
    """
    Generate full URL for file
    
    Args:
        file_path: Relative file path
        request_base_url: Base URL of the request
        
    Returns:
        Full URL to file or None if no file path
    """
    if not file_path:
        return None
    
    # Remove leading slash if present
    if file_path.startswith("/"):
        file_path = file_path[1:]
    
    return f"{request_base_url}/{file_path}"

def get_default_image_url(request_base_url: str = "") -> str:
    """
    Get URL for default image
    
    Args:
        request_base_url: Base URL of the request
        
    Returns:
        URL to default image
    """
    return f"{request_base_url}/static/default/no-image.svg"

def validate_pagination_params(skip: int, limit: int) -> tuple[int, int]:
    """
    Validate and adjust pagination parameters
    
    Args:
        skip: Number of records to skip
        limit: Number of records to return
        
    Returns:
        Tuple of validated (skip, limit)
    """
    # Ensure skip is not negative
    skip = max(0, skip)
    
    # Ensure limit is within allowed range
    limit = max(1, min(limit, settings.max_page_size))
    
    return skip, limit

def generate_search_filters(
    search_term: str, 
    searchable_fields: List[str], 
    model_class: Any
) -> List[Any]:
    """
    Generate search filters for SQLAlchemy query
    
    Args:
        search_term: Search term
        searchable_fields: List of field names to search in
        model_class: SQLAlchemy model class
        
    Returns:
        List of SQLAlchemy filter conditions
    """
    from sqlalchemy import or_
    
    filters = []
    for field_name in searchable_fields:
        if hasattr(model_class, field_name):
            field = getattr(model_class, field_name)
            filters.append(field.contains(search_term))
    
    return [or_(*filters)] if filters else []

def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted file size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    
    return f"{s} {size_names[i]}"

def clean_html_content(content: str) -> str:
    """
    Clean HTML content for safe display
    
    Args:
        content: HTML content string
        
    Returns:
        Cleaned content string
    """
    import html
    import re
    
    # Remove HTML tags
    clean_text = re.sub('<.*?>', '', content)
    
    # Decode HTML entities
    clean_text = html.unescape(clean_text)
    
    # Remove extra whitespace
    clean_text = ' '.join(clean_text.split())
    
    return clean_text

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to specified length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix
