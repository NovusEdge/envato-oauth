# Envato API OAuth Implementation

Complete OAuth 2.0 implementation for the Envato API with **one-function authentication**.

## 🚀 Simple Usage (Recommended)

```python
from envato_oauth import authenticate
import requests

# One function call handles all OAuth complexity
token = authenticate()

# Use token for API calls
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(
    "https://api.envato.com/v1/market/private/user/account.json",
    headers=headers
)
```

## 📦 Module Interface

The `envato_oauth` module provides these simple functions:

- `authenticate()` - One-function OAuth (handles everything automatically)
- `get_auth_headers()` - Get headers ready for API requests  
- `is_authenticated()` - Check authentication status
- `clear_authentication()` - Clear stored tokens

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your Envato API credentials
   ```

3. **Start localtunnel (for external access):**
   ```bash
   lt --port 56654 --subdomain seamless-themes
   ```

4. **Authenticate (choose one method):**
   
   **Option A: Web-based (recommended)**
   ```bash
   python oauth_server.py
   ```
   
   **Option B: CLI-based**
   ```bash
   python oauth_cli.py
   ```

5. **Test the module:**
   ```bash
   python example_simple.py
   ```

## Advanced Usage

For more control, you can still use the individual scripts:

## Environment Configuration

Create a `.env` file:

```env
ENVATO_CLIENT_ID=your_client_id_here
ENVATO_CLIENT_SECRET=your_client_secret_here
OAUTH_PORT=56654
ENVATO_REDIRECT_URI=https://seamless-themes.loca.lt/callback
```

## Core Files

- `envato_oauth.py` - **Main module** - One-function OAuth interface
- `example_simple.py` - Simple usage example
- `auth.py` - OAuth implementation (used internally)
- `oauth_server.py` - FastAPI web server for OAuth flow
- `oauth_cli.py` - CLI-based OAuth authentication
- `api_client_example.py` - Advanced API usage example
- `.envato.auth.json` - Secure token storage (auto-created)

## Features

✅ Configurable OAuth port via `OAUTH_PORT` environment variable  
✅ Automatic token refresh and storage  
✅ Web-based authentication flow  
✅ Localtunnel integration  
✅ Secure token management

## API Usage Example

```python
from envato_oauth import authenticate, get_auth_headers
import requests

# Method 1: Get token directly
token = authenticate()
headers = {"Authorization": f"Bearer {token}"}

# Method 2: Get headers directly  
headers = get_auth_headers()

# Method 3: Advanced options
token = authenticate(
    method="manual",        # Force manual auth
    force_reauth=True,     # Force re-authentication
    quiet=True            # Silent mode
)

# Make API calls
response = requests.get(
    "https://api.envato.com/v1/market/private/user/account.json",
    headers=headers
)
```

## 🌐 Browser-Based OAuth Server

For the easiest authentication experience, use the FastAPI-based OAuth server that automatically launches your browser:

```bash
# Run the OAuth server (launches browser automatically)
python oauth_server.py
```

This will:
1. Start a local FastAPI server on `http://localhost:8080`
2. Open your browser to the Envato authorization page
3. Handle the OAuth callback automatically
4. Store your tokens securely in `.envato.auth.json`
5. Confirm successful authentication

### Using the OAuth Server Programmatically

```python
from oauth_server import authenticate_with_browser
from envato_oauth import get_envato_auth_headers
import requests

# Authenticate using browser flow
if authenticate_with_browser():
    # Make authenticated API calls
    headers = get_envato_auth_headers()
    response = requests.get(
        "https://api.envato.com/v1/market/user:username.json",
        headers=headers
    )
    print(response.json())
```
