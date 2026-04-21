import pytest
from github_user import GitHubUser

def test_github_user_stats():
    repos = [
        {"name": "repo1", "language": "Python"},
        {"name": "repo2", "language": "JavaScript"},
        {"name": "repo3", "language": "Python"},
        {"name": "repo4", "language": None},
    ]
    user = GitHubUser("testuser", followers=10, repos=repos)
    
    assert user.get_most_used_language() == "Python"
    assert user.get_all_technologies() == ["JavaScript", "Python"]
    assert user.followers == 10
    assert user.is_partial is False

def test_github_user_deep_stats():
    repos = [
        {
            "name": "repo1", 
            "language": "Python", 
            "languages": {"Python": 100, "C++": 50}
        },
        {
            "name": "repo2", 
            "language": "JavaScript", 
            "languages": {"JavaScript": 200, "TypeScript": 100}
        }
    ]
    user = GitHubUser("testuser", repos=repos)
    
    # most used remains based on primary language per current logic
    assert user.get_most_used_language() == "Python"
    # all technologies now includes all languages from the dicts
    assert "C++" in user.get_all_technologies()
    assert "TypeScript" in user.get_all_technologies()
    assert user.get_all_technologies() == ["C++", "JavaScript", "Python", "TypeScript"]

def test_github_user_partial_flag():
    user = GitHubUser("testuser", is_partial=True)
    data = user.to_dict()
    assert data["is_partial"] is True

def test_github_user_no_repos():
    user = GitHubUser("testuser", followers=10, repos=[])
    assert user.get_most_used_language() is None
    assert user.get_all_technologies() == []

def test_github_user_no_languages():
    repos = [{"name": "repo1", "language": None, "languages": {}}]
    user = GitHubUser("testuser", followers=10, repos=repos)
    assert user.get_most_used_language() is None
    assert user.get_all_technologies() == []
