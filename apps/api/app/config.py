import os
from dotenv import load_dotenv

load_dotenv()

FORCE_DB_ERROR = False
class Settings:
    def __init__(self):
        self.PORT = self._load_port()
        self.DATABASE_URL = self._load_database_url()
        self.API_KEY_A = self._require("API_KEY_A")
        self.API_KEY_B = self._require("API_KEY_B")
        self.REDIS_URL = os.getenv("REDIS_URL")  # optional for now
        self.JWT_SECRET = os.getenv("JWT_SECRET")  # unused for now

    def _require(self, key: str):
        value = os.getenv(key)
        if not value:
            raise ValueError(f"{key} is required but not set.")
        return value

    def _load_port(self):
        value = os.getenv("PORT")
        if value is None or value == "":
            return 8000

        try:
            port = int(value)
        except ValueError:
            raise ValueError(f"PORT must be an integer, got '{value}'")

        if not (1024 <= port <= 65535):
            raise ValueError(f"PORT={port} is invalid. Must be 1024-65535")

        return port

    def _load_database_url(self):
        value = os.getenv("DATABASE_URL")
        if not value:
            raise ValueError("DATABASE_URL is required but not set.")
        return value


settings = Settings()