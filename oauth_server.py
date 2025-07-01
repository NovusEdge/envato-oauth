#!/usr/bin/env python3
"""
OAuth Server Script for Envato API Authentication
Launches a FastAPI server and browser to complete OAuth flow.
"""

import webbrowser
import threading
import time
import sys
import asyncio
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from auth import EnvatoAuth
import os
import dotenv

# Load .env file but don't override existing environment variables
dotenv.load_dotenv(override=False)

# Global variables for the FastAPI app
app = FastAPI(title="Envato OAuth Server", description="OAuth callback handler for Envato API")
oauth_result = {"code": None, "error": None, "completed": False}

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Envato OAuth Server is running. Waiting for callback..."}

@app.get("/callback")
async def oauth_callback(request: Request):
    """Handle OAuth callback from Envato"""
    global oauth_result
    
    # Get query parameters
    query_params = dict(request.query_params)
    
    if "code" in query_params:
        oauth_result["code"] = query_params["code"]
        oauth_result["completed"] = True
        
        success_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Authentication Successful</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; margin: 50px; }
                .success { color: #28a745; font-size: 24px; margin: 20px 0; }
                .message { font-size: 16px; color: #555; }
                .close-btn { 
                    background: #007bff; color: white; padding: 10px 20px; 
                    border: none; border-radius: 5px; cursor: pointer; margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <div class="success">✅ Authentication Successful!</div>
            <div class="message">
                <p>You have successfully authenticated with Envato.</p>
                <p>You can now close this browser window and return to your application.</p>
            </div>
            <button class="close-btn" onclick="window.close()">Close Window</button>
        </body>
        </html>
        """
        return HTMLResponse(content=success_html, status_code=200)
        
    elif "error" in query_params:
        oauth_result["error"] = query_params.get("error", "Unknown error")
        oauth_result["completed"] = True
        
        error = query_params.get("error", "Unknown error")
        error_description = query_params.get("error_description", "No description provided")
        
        error_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Authentication Failed</title>
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; margin: 50px; }}
                .error {{ color: #dc3545; font-size: 24px; margin: 20px 0; }}
                .message {{ font-size: 16px; color: #555; }}
                .details {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="error">❌ Authentication Failed</div>
            <div class="message">
                <p>There was an error during authentication:</p>
                <div class="details">
                    <strong>Error:</strong> {error}<br>
                    <strong>Description:</strong> {error_description}
                </div>
                <p>Please close this window and try again.</p>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=error_html, status_code=400)
    else:
        oauth_result["error"] = "Missing authorization code or error parameter"
        oauth_result["completed"] = True
        raise HTTPException(status_code=400, detail="Missing authorization code or error parameter")

@app.get("/app/envato/callback")
async def oauth_callback_path(request: Request):
    """Handle OAuth callback from Envato (with path)"""
    return await oauth_callback(request)

@app.get("/status")
async def status():
    """Check server status and OAuth completion state"""
    global oauth_result
    return {
        "server": "running",
        "oauth_completed": oauth_result["completed"],
        "has_code": oauth_result["code"] is not None,
        "has_error": oauth_result["error"] is not None
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "envato-oauth-server"}

class OAuthServer:
    """FastAPI OAuth server for handling authentication"""
    
    def __init__(self, port=None):
        # Use OAUTH_PORT from environment, fallback to 56654
        if port is None:
            port = int(os.getenv("OAUTH_PORT", "56654"))
        self.port = port
        self.server_process = None
        self.server_thread = None
    
    def start_server(self):
        """Start the FastAPI OAuth server"""
        global oauth_result
        oauth_result = {"code": None, "error": None, "completed": False}
        
        try:
            print(f"🚀 Starting FastAPI OAuth server on http://localhost:{self.port}")
            
            # Configure uvicorn to run without logs in the main thread
            config = uvicorn.Config(
                app=app,
                host="127.0.0.1",  # Bind only to IPv4 localhost
                port=self.port,
                log_level="error",  # Minimize logging
                access_log=False
            )
            
            # Start server in a separate thread
            self.server_thread = threading.Thread(
                target=self._run_server,
                args=(config,),
                daemon=True
            )
            self.server_thread.start()
            
            # Give the server a moment to start
            time.sleep(1)
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            return False
    
    def _run_server(self, config):
        """Run the FastAPI server"""
        try:
            server = uvicorn.Server(config)
            asyncio.run(server.serve())
        except Exception as e:
            print(f"❌ Server error: {e}")
    
    def wait_for_auth(self, timeout=300):
        """Wait for authentication to complete"""
        global oauth_result
        start_time = time.time()
        
        while not oauth_result["completed"]:
            if time.time() - start_time > timeout:
                print(f"⏰ Authentication timed out after {timeout} seconds")
                return None
            
            time.sleep(0.5)
        
        return oauth_result["code"] if oauth_result["code"] else None
    
    def stop_server(self):
        """Stop the OAuth server"""
        # The server will stop when the main process ends
        pass

def authenticate_with_browser():
    """
    Complete OAuth flow by launching browser and local server
    
    Returns:
        bool: True if authentication successful, False otherwise
    """
    try:
        # Initialize Envato Auth
        auth = EnvatoAuth()
        
        # Check if already authenticated
        if auth.is_authenticated():
            print("✅ Already authenticated!")
            token_preview = auth.get_valid_access_token()
            if token_preview:
                print(f"🔑 Current token: {token_preview[:20]}...")
            return True
        
        print("🔐 Starting Envato OAuth authentication...")
        
        os.getenv("OAUTH_PORT", "8080")  # Ensure port is set for redirect URI
        # Start local server
        server = OAuthServer()
        if not server.start_server():
            return False
        
        try:
            # Get authorization URL
            auth_url = auth.get_auth_url()
            print(f"🌐 Opening browser to: {auth_url}")
            
            # Open browser
            if not webbrowser.open(auth_url):
                print("❌ Failed to open browser automatically.")
                print(f"Please manually open this URL in your browser: {auth_url}")
            
            print("⏳ Waiting for authentication...")
            print("   (Please complete the authentication in your browser)")
            
            # Wait for callback
            auth_code = server.wait_for_auth()
            
            if auth_code:
                print("✅ Authorization code received!")
                print("🔄 Exchanging code for access token...")
                
                # Exchange code for tokens
                token_data = auth.exchange_code_for_tokens(auth_code)
                
                if token_data and "access_token" in token_data:
                    print("🎉 Authentication successful!")
                    print(f"🔑 Access token: {token_data['access_token'][:20]}...")
                    
                    if "expires_in" in token_data:
                        print(f"⏰ Token expires in: {token_data['expires_in']} seconds")
                    
                    return True
                else:
                    print("❌ Failed to get access token from authorization code")
                    return False
            else:
                print("❌ No authorization code received")
                return False
                
        finally:
            server.stop_server()
            
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Envato OAuth Authentication Tool")
    print("=" * 40)
    
    try:
        # Check for existing authentication
        auth = EnvatoAuth()
        
        if auth.is_authenticated():
            print("✅ You are already authenticated!")
            
            # Show current auth info
            info = auth.get_auth_info()
            if 'token_preview' in info and info['token_preview']:
                print(f"🔑 Current token: {info['token_preview']}")
            
            # Ask if user wants to re-authenticate
            response = input("\n🤔 Do you want to authenticate again? (y/N): ").strip().lower()
            if response not in ['y', 'yes']:
                print("👋 Keeping existing authentication. Goodbye!")
                return
            
            # Clear existing authentication
            print("🗑️  Clearing existing authentication...")
            auth.revoke_tokens()
        
        # Perform authentication
        success = authenticate_with_browser()
        
        if success:
            print("\n🎊 All done! You can now use the Envato API.")
            print("💡 Use the functions in envato_oauth.py to make authenticated requests.")
        else:
            print("\n💥 Authentication failed. Please try again.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n👋 Authentication cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
