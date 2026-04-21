import os
import sys
# Add the current directory (backend/) to sys.path to resolve imports on Render
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import re
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from github_api import get_user_data, get_user_repos
from github_user import GitHubUser
from settings import get_shared_config, ALLOWED_ORIGINS


limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/config")
def get_config():
    return get_shared_config()

@app.get("/api/user")
@limiter.limit("10/minute")
def get_user(request: Request, username: str, deep: bool = False):
    # Validate username (GitHub rules: alphanumeric, hyphens, max 39 chars)
    if not re.match(r"^[a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){0,38}$", username):
        raise HTTPException(status_code=400, detail="Invalid GitHub username format")

    user_response = get_user_data(username)
    if user_response.status_code == 404:
        raise HTTPException(status_code=404, detail=f"User '{username}' not found")
    elif user_response.status_code in [403, 429]:
        raise HTTPException(status_code=403, detail="GitHub API rate limit exceeded. Please try again later.")
    elif user_response.status_code != 200:
        raise HTTPException(status_code=user_response.status_code, detail="Failed to fetch user data from GitHub")

    user_data = user_response.json()

    repos_data, is_partial = get_user_repos(username, deep=deep)
    
    user = GitHubUser(
        username=username,
        followers=user_data.get("followers", 0),
        repos=repos_data,
        bio=user_data.get("bio"),
        company=user_data.get("company"),
        location=user_data.get("location"),
        blog=user_data.get("blog"),
        is_partial=is_partial
    )
    
    return user.to_dict()
