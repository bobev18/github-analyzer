import requests
from concurrent.futures import ThreadPoolExecutor
from settings import GITHUB_TOKEN, GITHUB_AUTH_ENABLED as AUTH_ENABLED

BASE_URL = "https://api.github.com"


def get_headers():
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "GitHub-Analyzer-App"
    }
    if GITHUB_TOKEN and AUTH_ENABLED:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    return headers


def get_user_data(username):
    """
    Fetch user data from GitHub API.
    Returns: response object
    """
    url = f"{BASE_URL}/users/{username}"
    return requests.get(url, headers=get_headers())


def get_repo_languages(owner, repo):
    """
    Fetch languages for a specific repository.
    """
    url = f"{BASE_URL}/repos/{owner}/{repo}/languages"
    response = requests.get(url, headers=get_headers())
    if response.status_code == 200:
        return response.json()
    response.raise_for_status()


def get_user_repos(username, deep=False):
    """
    call the GitHub API and return a list of dicts(repos name, language/technology) with data or None.
    If deep=True, also fetches all languages for each repo.
    """
    repos_data = []
    page = 1
    is_partial = False
    
    while True:
        url = f"{BASE_URL}/users/{username}/repos?per_page=100&page={page}"
        try:
            response = requests.get(url, headers=get_headers())
            if response.status_code != 200:
                break
            
            page_data = response.json()
            if not page_data:
                break
                
            repos_data.extend(page_data)
            if len(page_data) < 100:
                break
            page += 1
        except Exception:
            is_partial = True
            break

    if not repos_data and page == 1:
        return None, False

    result_repos = []
    
    def process_repo(r):
        nonlocal is_partial
        repo_info = {"name": r["name"], "language": r["language"], "languages": {}}
        if deep:
            try:
                repo_info["languages"] = get_repo_languages(username, r["name"])
            except Exception:
                is_partial = True
        return repo_info

    if deep:
        if AUTH_ENABLED:
            with ThreadPoolExecutor(max_workers=10) as executor:
                result_repos = list(executor.map(process_repo, repos_data))
        else:
            for r in repos_data:
                result_repos.append(process_repo(r))
                if is_partial: # Stop early if we hit rate limits in sequential mode
                    break
    else:
        result_repos = [{"name": r["name"], "language": r["language"], "languages": {}} for r in repos_data]

    return result_repos, is_partial