import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_JSON_PATH = BASE_DIR / "project.json"

def load_project_config():
    if PROJECT_JSON_PATH.exists():
        try:
            with open(PROJECT_JSON_PATH, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading project.json: {e}")
    return {}

_config = load_project_config()

# Secrets from .env
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Shared settings from project.json (with .env fallback for transition)
GITHUB_AUTH_ENABLED = _config.get("github_auth_enabled", 
                                  os.getenv("GITHUB_AUTH_ENABLED", "true").lower() == "true")

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:4200").split(",")


def get_shared_config():
    """Returns only non-sensitive configuration."""
    return {
        "github_auth_enabled": GITHUB_AUTH_ENABLED
    }
