"""
Configuration loader for environment variables required throughout the app.

Loads and validates essential API keys and credentials from a `.env` file:
- TMDB API key
- OpenRouter API key
- Email address and password
"""
import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self.tmdb_api_key = os.getenv('TMDB_API_KEY')
        self.openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
        self.email_address = os.getenv('EMAIL_ADDRESS')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self._validate()

    def _validate(self):
        if not self.tmdb_api_key:
            raise ValueError("TMDB_API_KEY is missing.")
        if not self.openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY is missing.")
        if not self.email_address or not self.email_password:
            raise ValueError("Email credentials are missing.")
