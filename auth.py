import requests
from typing import Optional, Dict, Any
import dotenv
import json
import os
from datetime import datetime, timedelta
import urllib.parse

dotenv.load_dotenv(override=True)

class EnvatoAuth:
    def __init__(self, token_file: str = ".envato.auth.json"):
        self.client_id = os.getenv("ENVATO_CLIENT_ID")
        self.client_secret = os.getenv("ENVATO_CLIENT_SECRET")
        self.redirect_uri = os.getenv("ENVATO_REDIRECT_URI")
        self.token_file = token_file
        self.tokens = self._load_tokens()
        
        if not all([self.client_id, self.client_secret, self.redirect_uri]):
            raise ValueError("Missing required environment variables: ENVATO_CLIENT_ID, ENVATO_CLIENT_SECRET, ENVATO_REDIRECT_URI")

    def get_auth_url(self) -> str:
        """Generate the authorization URL for OAuth flow"""
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri
        }
        return f"https://api.envato.com/authorization?{urllib.parse.urlencode(params)}"
    
    def exchange_code_for_tokens(self, authorization_code: str) -> Dict[str, Any]:
        """Exchange authorization code for access and refresh tokens"""
        token_url = "https://api.envato.com/token"
        
        # Try both methods - first as form data (more standard for OAuth)
        data = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri
        }
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        try:
            response = requests.post(token_url, data=data, headers=headers)
            response.raise_for_status()
            
            token_data = response.json()
            
            # Add expiry timestamp
            if "expires_in" in token_data:
                expires_at = datetime.now() + timedelta(seconds=token_data["expires_in"])
                token_data["expires_at"] = expires_at.isoformat()
            
            self.tokens = token_data
            self._save_tokens()
            
            return token_data
            
        except requests.RequestException as e:
            # If form data fails, try query parameters as shown in Envato docs
            try:
                params = {
                    "grant_type": "authorization_code",
                    "code": authorization_code,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "redirect_uri": self.redirect_uri
                }
                
                query_url = f"{token_url}?{urllib.parse.urlencode(params)}"
                response = requests.post(query_url)
                response.raise_for_status()
                
                token_data = response.json()
                
                # Add expiry timestamp
                if "expires_in" in token_data:
                    expires_at = datetime.now() + timedelta(seconds=token_data["expires_in"])
                    token_data["expires_at"] = expires_at.isoformat()
                
                self.tokens = token_data
                self._save_tokens()
                
                return token_data
                
            except requests.RequestException as e2:
                # Add more detailed error information
                error_msg = f"Failed to exchange code for tokens (both methods tried): {e2}"
                if hasattr(e2, 'response') and e2.response is not None:
                    try:
                        error_detail = e2.response.json()
                        error_msg += f" - Response: {error_detail}"
                    except:
                        error_msg += f" - Response text: {e2.response.text}"
                raise Exception(error_msg)
    
    def refresh_access_token(self) -> Dict[str, Any]:
        """Refresh the access token using the refresh token"""
        if not self.tokens or "refresh_token" not in self.tokens:
            raise Exception("No refresh token available. Re-authorization required.")
        
        params = {
            "grant_type": "refresh_token",
            "refresh_token": self.tokens["refresh_token"],
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        token_url = f"https://api.envato.com/token?{urllib.parse.urlencode(params)}"
        
        try:
            response = requests.post(token_url)
            response.raise_for_status()
            
            token_data = response.json()
            
            # Add expiry timestamp
            if "expires_in" in token_data:
                expires_at = datetime.now() + timedelta(seconds=token_data["expires_in"])
                token_data["expires_at"] = expires_at.isoformat()
            
            # Keep the refresh token if not provided in response
            if "refresh_token" not in token_data and "refresh_token" in self.tokens:
                token_data["refresh_token"] = self.tokens["refresh_token"]
            
            self.tokens = token_data
            self._save_tokens()
            
            return token_data
            
        except requests.RequestException as e:
            raise Exception(f"Failed to refresh access token: {e}")
    
    def get_valid_access_token(self) -> Optional[str]:
        """Get a valid access token, refreshing if necessary"""
        if not self.tokens:
            return None
        
        # Check if token is expired
        if self._is_token_expired():
            try:
                self.refresh_access_token()
            except Exception:
                return None
        
        return self.tokens.get("access_token")
    
    def _is_token_expired(self) -> bool:
        """Check if the current access token is expired"""
        if not self.tokens or "expires_at" not in self.tokens:
            return True
        
        try:
            expires_at = datetime.fromisoformat(self.tokens["expires_at"])
            # Consider token expired 5 minutes before actual expiry
            return datetime.now() >= (expires_at - timedelta(minutes=5))
        except (ValueError, TypeError):
            return True
    
    def _load_tokens(self) -> Optional[Dict[str, Any]]:
        """Load tokens from the token file"""
        if os.path.exists(self.token_file):
            try:
                with open(self.token_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return None
        return None
    
    def _save_tokens(self) -> None:
        """Save tokens to the token file"""
        if self.tokens:
            try:
                with open(self.token_file, 'w') as f:
                    json.dump(self.tokens, f, indent=2)
                # Set file permissions to be readable only by owner
                os.chmod(self.token_file, 0o600)
            except IOError as e:
                raise Exception(f"Failed to save tokens: {e}")
    
    def revoke_tokens(self) -> bool:
        """Revoke the current tokens and clear stored data"""
        if not self.tokens or "access_token" not in self.tokens:
            return True
        
        # Note: Envato API doesn't have a standard revoke endpoint documented
        # So we'll just clear local tokens
        self.tokens = None
        
        # Remove token file
        if os.path.exists(self.token_file):
            try:
                os.remove(self.token_file)
            except OSError:
                pass
        
        return True
    
    def is_authenticated(self) -> bool:
        """Check if user is currently authenticated"""
        return self.get_valid_access_token() is not None
    
    def get_auth_headers(self) -> Dict[str, str]:
        """Get headers with authorization for API requests"""
        token = self.get_valid_access_token()
        if not token:
            raise Exception("No valid access token. Authentication required.")
        
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def get_auth_info(self) -> Dict[str, Any]:
        """
        Get authentication status and token information.
        
        Returns:
            dict: Authentication information including status, token preview, etc.
        """
        try:
            authenticated = self.is_authenticated()
            
            result = {
                "authenticated": authenticated,
                "token_file": self.token_file,
                "token_preview": None,
                "client_id": self.client_id[:10] + "..." if self.client_id else None
            }
            
            if authenticated:
                token = self.get_valid_access_token()
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