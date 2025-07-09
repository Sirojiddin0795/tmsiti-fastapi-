from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import Callable
from app.core.config import settings
import json
import os

class LanguageMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle language detection and localization
    """
    
    def __init__(self, app):
        super().__init__(app)
        self.localization_cache = {}
        self._load_localization_files()
    
    def _load_localization_files(self):
        """Load localization files into cache"""
        localization_dir = "app/localization"
        
        for language in settings.supported_languages:
            file_path = os.path.join(localization_dir, f"{language}.json")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.localization_cache[language] = json.load(f)
            except FileNotFoundError:
                # Create empty localization if file doesn't exist
                self.localization_cache[language] = {}
            except json.JSONDecodeError:
                # Handle invalid JSON
                self.localization_cache[language] = {}
    
    def _detect_language(self, request: Request) -> str:
        """
        Detect language from request
        
        Priority:
        1. Query parameter 'lang'
        2. Header 'Accept-Language'
        3. Default language from settings
        """
        
        # Check query parameter
        lang_param = request.query_params.get('lang')
        if lang_param and lang_param in settings.supported_languages:
            return lang_param
        
        # Check Accept-Language header
        accept_language = request.headers.get('Accept-Language', '')
        
        # Parse Accept-Language header
        languages = []
        for lang_tag in accept_language.split(','):
            if ';' in lang_tag:
                lang, quality = lang_tag.split(';', 1)
                try:
                    quality_value = float(quality.split('=')[1])
                except (IndexError, ValueError):
                    quality_value = 1.0
            else:
                lang = lang_tag
                quality_value = 1.0
            
            lang = lang.strip().lower()
            
            # Extract language code (e.g., 'en' from 'en-US')
            if '-' in lang:
                lang = lang.split('-')[0]
            
            if lang in settings.supported_languages:
                languages.append((lang, quality_value))
        
        # Sort by quality value (descending)
        languages.sort(key=lambda x: x[1], reverse=True)
        
        # Return the highest quality supported language
        if languages:
            return languages[0][0]
        
        # Return default language
        return settings.default_language
    
    def _get_localized_text(self, key: str, language: str, **kwargs) -> str:
        """
        Get localized text for given key and language
        
        Args:
            key: Localization key
            language: Language code
            **kwargs: Variables for string formatting
            
        Returns:
            Localized text or key if not found
        """
        try:
            # Get text from cache
            localization = self.localization_cache.get(language, {})
            text = localization.get(key, key)
            
            # Format with variables if provided
            if kwargs:
                text = text.format(**kwargs)
            
            return text
        except Exception:
            return key
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and add language information"""
        
        # Detect language
        detected_language = self._detect_language(request)
        
        # Add language information to request state
        request.state.language = detected_language
        
        # Add localization function to request state
        def localize(key: str, **kwargs) -> str:
            return self._get_localized_text(key, detected_language, **kwargs)
        
        request.state.localize = localize
        
        # Add available languages to request state
        request.state.available_languages = settings.supported_languages
        
        # Process request
        response = await call_next(request)
        
        # Add language header to response
        response.headers["Content-Language"] = detected_language
        
        return response

def get_language_from_request(request: Request) -> str:
    """
    Helper function to get language from request
    
    Args:
        request: FastAPI Request object
        
    Returns:
        Language code
    """
    return getattr(request.state, 'language', settings.default_language)

def localize_text(request: Request, key: str, **kwargs) -> str:
    """
    Helper function to get localized text
    
    Args:
        request: FastAPI Request object
        key: Localization key
        **kwargs: Variables for string formatting
        
    Returns:
        Localized text
    """
    localize_func = getattr(request.state, 'localize', None)
    if localize_func:
        return localize_func(key, **kwargs)
    return key

def get_localized_model_field(obj, field_prefix: str, language: str) -> str:
    """
    Get localized field value from model object
    
    Args:
        obj: Model object
        field_prefix: Field prefix (e.g., 'title', 'content')
        language: Language code
        
    Returns:
        Localized field value
    """
    # Try exact language match
    field_name = f"{field_prefix}_{language}"
    value = getattr(obj, field_name, None)
    
    if value:
        return value
    
    # Try fallback languages
    for fallback_lang in settings.supported_languages:
        if fallback_lang != language:
            fallback_field = f"{field_prefix}_{fallback_lang}"
            fallback_value = getattr(obj, fallback_field, None)
            if fallback_value:
                return fallback_value
    
    return ""

class LocalizationHelper:
    """Helper class for localization operations"""
    
    @staticmethod
    def get_multilingual_dict(obj, field_prefix: str) -> dict:
        """
        Get multilingual dictionary for a field
        
        Args:
            obj: Model object
            field_prefix: Field prefix
            
        Returns:
            Dictionary with language codes as keys
        """
        result = {}
        for lang in settings.supported_languages:
            field_name = f"{field_prefix}_{lang}"
            value = getattr(obj, field_name, "")
            result[lang] = value
        return result
    
    @staticmethod
    def set_multilingual_field(obj, field_prefix: str, values: dict):
        """
        Set multilingual field values on object
        
        Args:
            obj: Model object
            field_prefix: Field prefix
            values: Dictionary with language codes as keys
        """
        for lang in settings.supported_languages:
            field_name = f"{field_prefix}_{lang}"
            if lang in values and hasattr(obj, field_name):
                setattr(obj, field_name, values[lang])
    
    @staticmethod
    def validate_multilingual_data(data: dict, required_languages: list = None) -> bool:
        """
        Validate multilingual data
        
        Args:
            data: Dictionary with language codes as keys
            required_languages: List of required languages
            
        Returns:
            True if valid, False otherwise
        """
        if required_languages is None:
            required_languages = settings.supported_languages
        
        for lang in required_languages:
            if lang not in data or not data[lang].strip():
                return False
        
        return True
