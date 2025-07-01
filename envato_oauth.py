"""
Simple Module Interface for Envato OAuth
Provides easy-to-use functions for getting access tokens and auth headers.
"""

from typing import Optional, Dict
from auth import EnvatoAuth

def get_envato_access_token() -> Optional[str]:
    """
    Get a valid Envato access token.
    
    Returns:
        str: Valid access token if authenticated, None otherwise
        
    Example:
        token = get_envato_access_token()
        if token:
            # Use token for API calls
            headers = {"Authorization": f"Bearer {token}"}
        else:
            # Need to authenticate first
            print("Please run authentication: python oauth_cli_headless.py")
    """
    try:
        auth = EnvatoAuth()
        return auth.get_valid_access_token()
    except Exception:
        return None

def get_envato_auth_headers() -> Optional[Dict[str, str]]:
    """
    Get HTTP headers with authorization for Envato API requests.
    
    Returns:
        dict: Headers with Authorization and Content-Type if authenticated, None otherwise
        
    Example:
        headers = get_envato_auth_headers()
        if headers:
            response = requests.get("https://api.envato.com/v1/market/user:username.json", headers=headers)
        else:
            print("Please run authentication: python oauth_cli_headless.py")
    """
    try:
        auth = EnvatoAuth()
        return auth.get_auth_headers()
    except Exception:
        return None

def is_authenticated() -> bool:
    """
    Check if user is currently authenticated.
    
    Returns:
        bool: True if authenticated with valid token, False otherwise
        
    Example:
        if is_authenticated():
            print("Ready to make API calls!")
        else:
            print("Please authenticate first")
    """
    try:
        auth = EnvatoAuth()
        return auth.is_authenticated()
    except Exception:
        return False

def get_auth_info() -> Dict[str, any]:
    """
    Get authentication status and token information.
    
    Returns:
        dict: Authentication information including status, token preview, etc.
        
    Example:
        info = get_auth_info()
        print(f"Authenticated: {info['authenticated']}")
        if info['authenticated']:
            print(f"Token: {info['token_preview']}")
    """
    try:
        auth = EnvatoAuth()
        authenticated = auth.is_authenticated()
        
        result = {
            "authenticated": authenticated,
            "token_file": auth.token_file,
            "token_preview": None,
            "client_id": auth.client_id[:10] + "..." if auth.client_id else None
        }
        
        if authenticated:
            token = auth.get_valid_access_token()
            if token:
                result["token_preview"] = token[:20] + "..."
        
        return result
        
    except Exception as e:
        return {
            "authenticated": False,
            "error": str(e),
            "token_file": None,
            "token_preview": None,
            "client_id": None
        }

def revoke_authentication() -> bool:
    """
    Revoke current authentication and clear stored tokens.
    
    Returns:
        bool: True if successfully revoked, False otherwise
        
    Example:
        if revoke_authentication():
            print("Authentication cleared successfully")
        else:
            print("Failed to clear authentication")
    """
    try:
        auth = EnvatoAuth()
        return auth.revoke_tokens()
    except Exception:
        return False

# Convenience aliases
get_token = get_envato_access_token
get_headers = get_envato_auth_headers
check_auth = is_authenticated
clear_auth = revoke_authentication
