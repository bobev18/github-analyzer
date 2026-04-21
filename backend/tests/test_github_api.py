import pytest
from unittest.mock import patch, MagicMock
from github_api import get_user_data, get_user_repos

@patch('requests.get')
def test_get_user_data_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"login": "octocat", "followers": 2000, "bio": "Hello"}
    mock_get.return_value = mock_response
    
    response = get_user_data("octocat")
    data = response.json()
    assert data["login"] == "octocat"
    assert data["followers"] == 2000
    assert data["bio"] == "Hello"

@patch('requests.get')
def test_get_user_data_not_found(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response
    
    response = get_user_data("nonexistent")
    assert response.status_code == 404

@patch('requests.get')
def test_get_user_repos_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"name": "repo1", "language": "Python"},
        {"name": "repo2", "language": "JavaScript"}
    ]
    mock_get.return_value = mock_response
    
    repos, is_partial = get_user_repos("octocat")
    assert len(repos) == 2
    assert repos[0]["name"] == "repo1"
    assert repos[1]["language"] == "JavaScript"
    assert is_partial is False

@patch('requests.get')
def test_get_user_repos_pagination(mock_get):
    # Mock two pages of results
    mock_response1 = MagicMock()
    mock_response1.status_code = 200
    mock_response1.json.return_value = [{"name": f"repo{i}", "language": "Python"} for i in range(100)]
    
    mock_response2 = MagicMock()
    mock_response2.status_code = 200
    mock_response2.json.return_value = [{"name": "repo101", "language": "JavaScript"}]
    
    mock_get.side_effect = [mock_response1, mock_response2]
    
    repos, is_partial = get_user_repos("octocat")
    assert len(repos) == 101
    assert repos[100]["name"] == "repo101"
    assert is_partial is False

@patch('requests.get')
def test_get_user_repos_deep_analysis_sequential(mock_get, monkeypatch):
    # Mock AUTH_ENABLED=False to trigger sequential path
    import github_api
    monkeypatch.setattr(github_api, "AUTH_ENABLED", False)
    
    mock_repos_resp = MagicMock()
    mock_repos_resp.status_code = 200
    mock_repos_resp.json.return_value = [{"name": "repo1", "language": "Python"}]
    
    mock_langs_resp = MagicMock()
    mock_langs_resp.status_code = 200
    mock_langs_resp.json.return_value = {"Python": 1000}
    
    mock_get.side_effect = [mock_repos_resp, mock_langs_resp]
    
    repos, is_partial = github_api.get_user_repos("octocat", deep=True)
    assert len(repos) == 1
    assert is_partial is False

@patch('requests.get')
def test_get_user_repos_rate_limit_handling(mock_get):
    # Mock repo list
    mock_repos_resp = MagicMock()
    mock_repos_resp.status_code = 200
    mock_repos_resp.json.return_value = [
        {"name": "repo1", "language": "Python"},
        {"name": "repo2", "language": "JS"}
    ]
    
    # Mock languages endpoint: first call succeeds, second fails with 403
    mock_langs_ok = MagicMock()
    mock_langs_ok.status_code = 200
    mock_langs_ok.json.return_value = {"Python": 100}
    
    mock_langs_fail = MagicMock()
    mock_langs_fail.status_code = 403 # Rate limit
    import requests
    mock_langs_fail.raise_for_status.side_effect = requests.exceptions.HTTPError("403 Client Error")
    
    mock_get.side_effect = [mock_repos_resp, mock_langs_ok, mock_langs_fail]
    
    # In sequential mode or concurrent mode, if an exception is raised it sets is_partial
    repos, is_partial = get_user_repos("octocat", deep=True)
    assert len(repos) == 2
    assert is_partial is True
    assert repos[0]["languages"] == {"Python": 100}
    assert repos[1]["languages"] == {} # Failed fetch leads to empty dict

@patch('requests.get')
def test_get_user_repos_empty(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = []
    mock_get.return_value = mock_response
    
    repos, is_partial = get_user_repos("octocat")
    assert repos is None
    assert is_partial is False
