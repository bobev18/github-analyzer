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

def test_github_user_no_repos():
    user = GitHubUser("testuser", followers=10, repos=[])
    assert user.get_most_used_language() is None
    assert user.get_all_technologies() == []

def test_github_user_no_languages():
    repos = [{"name": "repo1", "language": None}]
    user = GitHubUser("testuser", followers=10, repos=repos)
    assert user.get_most_used_language() is None
    assert user.get_all_technologies() == []
