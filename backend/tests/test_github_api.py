import pytest
from unittest.mock import patch, MagicMock
from github_api import get_user_data, get_user_repos

@patch('requests.get')
def test_get_user_data_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"login": "octocat", "followers": 2000, "bio": "Hello"}
    mock_get.return_value = mock_response
    
    data = get_user_data("octocat")
    assert data["login"] == "octocat"
    assert data["followers"] == 2000
    assert data["bio"] == "Hello"

@patch('requests.get')
def test_get_user_data_not_found(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response
    
    data = get_user_data("nonexistent")
    assert data is None

@patch('requests.get')
def test_get_user_repos_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"name": "repo1", "language": "Python"},
        {"name": "repo2", "language": "JavaScript"}
    ]
    mock_get.return_value = mock_response
    
    repos = get_user_repos("octocat")
    assert len(repos) == 2
    assert repos[0]["name"] == "repo1"
    assert repos[1]["language"] == "JavaScript"
