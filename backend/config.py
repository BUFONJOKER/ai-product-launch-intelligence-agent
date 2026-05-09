"""Configuration module for loading environment variables from .env file."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# API Keys
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
DB_URL = os.getenv("DB_URL")
DB_URL_API = os.getenv("DB_URL_API")
ACCESS_TOKEN_SECRET_KEY = os.getenv("ACCESS_TOKEN_SECRET_KEY")
# Other configurations
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
ENV = os.getenv("ENV", "development")

# Validate required API keys
if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY is not set in .env file")

if not DB_URL:
    raise ValueError("DB_URL is not set in .env file")

if not DB_URL_API:
    raise ValueError("DB_URL_API is not set in .env file")

if not ACCESS_TOKEN_SECRET_KEY:
    raise ValueError("ACCESS_TOKEN is not set in .env file")