#!/usr/bin/env python3
"""
Setup script for Envato OAuth Package
"""

from setuptools import setup, find_packages
import os
import sys

# Ensure we can import from the current directory
sys.path.insert(0, os.path.dirname(__file__))

try:
    from __init__ import __package_info__, __version__
except ImportError:
    # Fallback if __init__.py is not available during setup
    __version__ = "1.0.0"
    __package_info__ = {
        "name": "envato-oauth",
        "description": "Complete OAuth 2.0 implementation for Envato API",
        "author": "Envato API OAuth Package",
        "author_email": "khimanialiasgar@gmail.com",
        "url": "https://github.com/NovusEdge/envato-oauth",
        "license": "MIT",
    }

# Read README for long description
def read_readme():
    """Read README.md file for long description"""
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return __package_info__.get("description", "")

# Read requirements from requirements.txt
def read_requirements():
    """Read requirements from requirements.txt"""
    requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    requirements = []
    
    if os.path.exists(requirements_path):
        with open(requirements_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith("#"):
                    # Remove version constraints for setup.py (can be customized)
                    package = line.split("==")[0].split(">=")[0].split("<=")[0]
                    requirements.append(package)
    
    return requirements

# Core requirements (minimal set for the package to work)
core_requirements = [
    "fastapi>=0.115.0",
    "uvicorn>=0.35.0", 
    "requests>=2.31.0",
    "python-dotenv>=1.0.0",
]

# Development requirements
dev_requirements = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
]

# Optional requirements for enhanced functionality
optional_requirements = {
    "selenium": ["selenium>=4.15.0", "webdriver-manager>=4.0.0"],
    "dev": dev_requirements,
    "all": dev_requirements + ["selenium>=4.15.0", "webdriver-manager>=4.0.0"],
}

setup(
    name=__package_info__.get("name", "envato-oauth"),
    version=__version__,
    description=__package_info__.get("description", "Complete OAuth 2.0 implementation for Envato API"),
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author=__package_info__.get("author", "Envato API OAuth Package"),
    author_email=__package_info__.get("author_email", "support@example.com"),
    url=__package_info__.get("url", "https://github.com/yourusername/envato-oauth"),
    license=__package_info__.get("license", "MIT"),
    
    # Package discovery
    packages=find_packages(exclude=["tests*", "docs*", "examples*"]),
    py_modules=["auth", "envato_oauth", "oauth_server", "api_client_example", "oauth_example"],
    
    # Requirements
    install_requires=core_requirements,
    extras_require=optional_requirements,
    
    # Python version requirement
    python_requires=">=3.8",
    
    # Entry points for command-line usage
    entry_points={
        "console_scripts": [
            "envato-oauth=oauth_server:main",
            "envato-auth=oauth_server:main",
        ],
    },
    
    # Package data
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.json", ".env.example"],
    },
    
    # Classification
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9", 
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Framework :: FastAPI",
    ],
    
    # Keywords for PyPI
    keywords="envato oauth api fastapi authentication oauth2 envato-market",
    
    # Project URLs
    project_urls={
        "Documentation": __package_info__.get("url", "") + "/docs",
        "Source": __package_info__.get("url", ""),
        "Tracker": __package_info__.get("url", "") + "/issues",
    },
    
    # Zip safety
    zip_safe=False,
)
