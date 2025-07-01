# Package Installation & Usage Guide

## 📦 Installation Options

### Option 1: Install from Source (Development)
```bash
# Clone or download the package
cd /path/to/envato-api

# Install in development mode
pip install -e .

# Or install with optional dependencies
pip install -e ".[selenium,dev]"
```

### Option 2: Install as Package
```bash
# Install from local directory
pip install .

# Or build and install
python setup.py sdist bdist_wheel
pip install dist/envato-oauth-1.0.0.tar.gz
```

### Option 3: Direct Import (No Installation)
```python
# Add package directory to Python path
import sys
sys.path.insert(0, '/path/to/envato-api')

# Import directly
from envato_oauth import get_envato_auth_headers
```

## 🚀 Quick Usage

### As Installed Package
```python
# After installation with pip
import envato_oauth

# Authenticate using browser flow
envato_oauth.authenticate_with_browser()

# Get auth headers for API calls
headers = envato_oauth.get_envato_auth_headers()

# Check authentication status
if envato_oauth.is_authenticated():
    print("Ready to make API calls!")
```

### Command Line Usage
```bash
# After installation, use the command line tools
envato-oauth      # Start OAuth authentication
envato-auth       # Alternative command name
```

### Programmatic Usage
```python
from envato_oauth import OAuthServer, EnvatoAuth
import requests

# Manual server control
server = OAuthServer(port=8080)
server.start_server()

# Use the auth class directly
auth = EnvatoAuth()
if auth.is_authenticated():
    headers = auth.get_auth_headers()
    response = requests.get("https://api.envato.com/v1/market/user:username.json", headers=headers)
```

## 🔧 Environment Configuration

Create a `.env` file in your project:
```bash
ENVATO_CLIENT_ID=your_client_id_here
ENVATO_CLIENT_SECRET=your_client_secret_here
ENVATO_REDIRECT_URI=http://localhost:56654/callback
OAUTH_PORT=56654
```

## 📁 Package Structure

After installation, the package provides:
- `envato_oauth` - Main module with easy-to-use functions
- `oauth_server` - FastAPI server for OAuth flow
- `auth` - Core authentication logic
- Command line tools: `envato-oauth`, `envato-auth`

## 🔐 Token Storage

Tokens are automatically stored in:
- `.envato.auth.json` - Secure token file (created automatically)
- File permissions: `0o600` (readable only by owner)
- Automatic token refresh when expired

## 🧪 Testing Installation

```python
# Test the installation
try:
    import envato_oauth
    print(f"✅ Package version: {envato_oauth.__version__}")
    print(f"✅ Available functions: {envato_oauth.__all__}")
    
    # Test OAuth server
    from envato_oauth import OAuthServer
    server = OAuthServer()
    print(f"✅ OAuth server configured for port: {server.port}")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
```

## 📚 Documentation

For full API documentation, see:
- `README.md` - Complete usage guide
- Package docstrings - Inline documentation
- Example files: `oauth_example.py`, `api_client_example.py`
