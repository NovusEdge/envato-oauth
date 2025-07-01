#!/usr/bin/env python3
"""
Example demonstrating the Envato OAuth server usage
"""

from oauth_server import authenticate_with_browser
from envato_oauth import is_authenticated, get_envato_auth_headers
import requests

def main():
    print("🚀 Envato API OAuth Example")
    print("=" * 40)
    
    # Check if already authenticated
    if not is_authenticated():
        print("🔐 Not authenticated. Starting OAuth flow...")
        
        # Start OAuth authentication
        success = authenticate_with_browser()
        
        if not success:
            print("❌ Authentication failed!")
            return
    else:
        print("✅ Already authenticated!")
    
    # Test API call
    print("\n🧪 Testing API call...")
    
    try:
        headers = get_envato_auth_headers()
        if headers:
            # Make a test API call to get user info
            response = requests.get(
                "https://api.envato.com/v1/market/user:username.json",
                headers=headers
            )
            
            if response.status_code == 200:
                user_data = response.json()
                print(f"🎉 API call successful!")
                print(f"👤 Username: {user_data.get('username', 'N/A')}")
                print(f"📧 Email: {user_data.get('email', 'N/A')}")
                print(f"🏆 Sales: {user_data.get('sales', 'N/A')}")
            else:
                print(f"❌ API call failed: {response.status_code}")
                print(f"Response: {response.text}")
        else:
            print("❌ Failed to get auth headers")
            
    except Exception as e:
        print(f"❌ Error making API call: {e}")

if __name__ == "__main__":
    main()
