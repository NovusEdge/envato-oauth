"""
Envato API OAuth Package

A complete OAuth 2.0 implementation for the Envato API with FastAPI server support.

This package provides:
- Simple OAuth authentication with browser-based flow
- FastAPI server for handling OAuth callbacks
- Secure token storage and management
- Easy-to-use API client functions

Main modules:
- envato_oauth: Simple interface functions for OAuth operations
- oauth_server: FastAPI-based OAuth server with browser integration
- auth: Core OAuth authentication logic
"""

__version__ = "1.0.0"
__author__ = "Envato API OAuth Package"
__email__ = "khimanialiasgar@gmail.com"

# Import main functions for easy access
from .envato_oauth import (
    get_envato_access_token,
    get_envato_auth_headers,
    is_authenticated,
    get_auth_info,
    revoke_authentication,
    # Convenience aliases
    get_token,
    get_headers,
    check_auth,
    clear_auth
)

from .oauth_server import (
    authenticate_with_browser,
    OAuthServer
)

from .auth import EnvatoAuth

__all__ = [
    # Main OAuth functions
    "get_envato_access_token",
    "get_envato_auth_headers", 
    "is_authenticated",
    "get_auth_info",
    "revoke_authentication",
    
    # Convenience aliases
    "get_token",
    "get_headers", 
    "check_auth",
    "clear_auth",
    
    # OAuth server
    "authenticate_with_browser",
    "OAuthServer",
    
    # Core auth class
    "EnvatoAuth",
]

# Package metadata
__package_info__ = {
    "name": "envato-oauth",
    "version": __version__,
    "description": "Complete OAuth 2.0 implementation for Envato API",
    "long_description": __doc__,
    "author": __author__,
    "author_email": __email__,
    "url": "https://github.com/yourusername/envato-oauth",
    "license": "MIT",
    "keywords": ["envato", "oauth", "api", "fastapi", "authentication"],
    "classifiers": [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
}
