import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.github.com"
TOKEN = os.getenv("GITHUB_TOKEN")
AUTH_ENABLED = os.getenv("GITHUB_AUTH_ENABLED", "true").lower() == "true"


def get_headers():
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    if TOKEN and AUTH_ENABLED:
        headers["Authorization"] = f"token {TOKEN}"
    return headers

# TODO: Make the use of token optional in the calls to the API

def get_user_data(username):
    """
    call the GitHub API and return a dict with data or None
    """
    url = f"{BASE_URL}/users/{username}"
    response = requests.get(url, headers=get_headers())
    if response.status_code == 200:
        return response.json()
    return None


def get_user_repos(username):
    """
    call the GitHub API and return a list of dicts(repos name, language/technology) with data or None
    """
    url = f"{BASE_URL}/users/{username}/repos"
    response = requests.get(url, headers=get_headers())
    if response.status_code == 200:
        repos = response.json()
        return [{"name": r["name"], "language": r["language"]} for r in repos]
    return None