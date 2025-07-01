#!/usr/bin/env python3
"""
Advanced API Client Example for Envato API
This example shows a more comprehensive API client implementation.
"""

import requests
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
from envato_oauth import get_envato_auth_headers, is_authenticated

class EnvatoAPIClient:
    """Advanced Envato API client with error handling and convenience methods"""
    
    def __init__(self):
        self.base_url = "https://api.envato.com/v1"
        self.headers = None
        self._authenticate()
    
    def _authenticate(self):
        """Set up authentication headers"""
        if not is_authenticated():
            raise Exception("Not authenticated. Please run: python oauth_cli_headless.py")
        
        self.headers = get_envato_auth_headers()
        if not self.headers:
            raise Exception("Failed to get authentication headers")
    
    def _make_request(self, endpoint: str, method: str = "GET", params: Dict = None, data: Dict = None) -> Dict[str, Any]:
        """Make an authenticated API request"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=self.headers, params=params, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, headers=self.headers, params=params, json=data, timeout=30)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            # Handle response
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json(),
                    "status_code": response.status_code
                }
            elif response.status_code == 401:
                return {
                    "success": False,
                    "error": "Authentication failed",
                    "status_code": response.status_code,
                    "suggestion": "Try re-authenticating: python oauth_cli_headless.py"
                }
            elif response.status_code == 403:
                return {
                    "success": False,
                    "error": "Access forbidden",
                    "status_code": response.status_code,
                    "suggestion": "Check API permissions and scopes"
                }
            elif response.status_code == 429:
                return {
                    "success": False,
                    "error": "Rate limit exceeded",
                    "status_code": response.status_code,
                    "suggestion": "Wait before making more requests"
                }
            else:
                error_detail = "Unknown error"
                try:
                    error_data = response.json()
                    error_detail = error_data.get("error", str(error_data))
                except:
                    error_detail = response.text[:200]
                
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {error_detail}",
                    "status_code": response.status_code
                }
                
        except requests.RequestException as e:
            return {
                "success": False,
                "error": f"Network error: {e}",
                "status_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {e}",
                "status_code": None
            }
    
    def get_user_items(self, site: str = "themeforest") -> Dict[str, Any]:
        """Get user's items from a specific site"""
        return self._make_request(f"market/user-items-by-site:{site}.json")
    
    def get_user_collections(self) -> Dict[str, Any]:
        """Get user's collections"""
        return self._make_request("market/user-collections.json")
    
    def get_item_details(self, item_id: str) -> Dict[str, Any]:
        """Get details for a specific item"""
        return self._make_request(f"market/catalog/item?id={item_id}")
    
    def search_items(self, term: str, site: str = "themeforest", category: str = None) -> Dict[str, Any]:
        """Search for items"""
        params = {
            "term": term,
            "site": site
        }
        if category:
            params["category"] = category
            
        return self._make_request("discovery/search/search/item", params=params)
    
    def get_popular_items(self, site: str = "themeforest") -> Dict[str, Any]:
        """Get popular items from a site"""
        return self._make_request(f"discovery/search/search/item", params={"site": site, "sort_by": "sales"})

def print_response(result: Dict[str, Any], title: str = "API Response"):
    """Pretty print API response"""
    print(f"\n📡 {title}")
    print("-" * 50)
    
    if result["success"]:
        print("✅ Success!")
        data = result["data"]
        
        # Try to extract meaningful information
        if isinstance(data, dict):
            # Count items if it's a collection
            for key in data.keys():
                if isinstance(data[key], list):
                    print(f"📊 {key}: {len(data[key])} items")
                elif isinstance(data[key], dict):
                    print(f"📄 {key}: {len(data[key])} fields")
                else:
                    print(f"📝 {key}: {data[key]}")
        
        # Show first few items if it's a list
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, list) and len(value) > 0:
                    print(f"\n🔍 First items from {key}:")
                    for i, item in enumerate(value[:3]):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('title', f'Item {i+1}'))
                            item_id = item.get('id', 'N/A')
                            print(f"   {i+1}. {name} (ID: {item_id})")
                        else:
                            print(f"   {i+1}. {item}")
                    
                    if len(value) > 3:
                        print(f"   ... and {len(value) - 3} more")
                    break
    else:
        print("❌ Failed!")
        print(f"   Error: {result['error']}")
        if "suggestion" in result:
            print(f"   💡 {result['suggestion']}")

def main():
    """Main example function"""
    print("🚀 Envato API Advanced Client Example")
    print("=" * 50)
    
    try:
        # Initialize API client
        print("🔧 Initializing API client...")
        client = EnvatoAPIClient()
        print("✅ API client ready!")
        
        # Example 1: Get user items
        print("\n📋 Example 1: Get User Items")
        result = client.get_user_items("themeforest")
        print_response(result, "User Items from ThemeForest")
        
        # Example 2: Get user collections
        print("\n📚 Example 2: Get User Collections")
        result = client.get_user_collections()
        print_response(result, "User Collections")
        
        # Example 3: Search for items
        print("\n🔍 Example 3: Search Items")
        result = client.search_items("wordpress", "themeforest")
        print_response(result, "Search Results for 'wordpress'")
        
        # Example 4: Get popular items
        print("\n🔥 Example 4: Popular Items")
        result = client.get_popular_items("themeforest")
        print_response(result, "Popular Items on ThemeForest")
        
        print("\n🎉 All examples completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Troubleshooting:")
        print("   • Make sure you're authenticated: python oauth_cli_headless.py")
        print("   • Check your internet connection")
        print("   • Verify your Envato API credentials")
    
    print("\n📖 More examples:")
    print("   python example_simple.py     - Simple API usage")
    print("   python oauth_cli_headless.py - Re-authenticate")

if __name__ == "__main__":
    main()
