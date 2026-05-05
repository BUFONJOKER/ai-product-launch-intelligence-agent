"""Configuration module for loading environment variables from .env file."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# API Keys
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


# Other configurations
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
ENV = os.getenv("ENV", "development")

# Validate required API keys
if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY is not set in .env file")

