from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from github_api import get_user_data, get_user_repos
from github_user import GitHubUser
from settings import get_shared_config


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/config")
def get_config():
    return get_shared_config()

@app.get("/api/user")
def get_user(username: str, deep: bool = False):
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
