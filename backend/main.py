from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from github_api import get_user_data, get_user_repos
from github_user import GitHubUser


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/user")
def get_user(username: str):
    user_data = get_user_data(username)
    if not user_data:
        raise HTTPException(status_code=404, detail=f"User '{username}' not found")

    repos_data = get_user_repos(username)
    
    user = GitHubUser(
        username=username,
        followers=user_data.get("followers", 0),
        repos=repos_data,
        bio=user_data.get("bio"),
        company=user_data.get("company"),
        location=user_data.get("location"),
        blog=user_data.get("blog")
    )
    
    return user.to_dict()