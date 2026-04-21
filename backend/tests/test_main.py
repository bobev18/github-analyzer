import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)

@patch('main.get_user_data')
@patch('main.get_user_repos')
def test_get_user_endpoint_basic(mock_repos, mock_user):
    # Mock user response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "login": "testuser",
        "followers": 5,
        "bio": "Test bio"
    }
    mock_user.return_value = mock_response
    
    # Mock repos data (return tuple: repos, is_partial)
    mock_repos.return_value = ([
        {"name": "repo1", "language": "Python", "languages": {}}
    ], False)
    
    response = client.get("/api/user?username=testuser")
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["followers"] == 5
    assert data["is_partial"] is False
    assert len(data["repos"]) == 1

@patch('main.get_user_data')
@patch('main.get_user_repos')
def test_get_user_endpoint_deep(mock_repos, mock_user):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"login": "testuser", "followers": 5}
    mock_user.return_value = mock_response
    mock_repos.return_value = ([], False)
    
    # Call with deep=true
    response = client.get("/api/user?username=testuser&deep=true")
    assert response.status_code == 200
    
    # Verify mock was called with deep=True
    mock_repos.assert_called_with("testuser", deep=True)

@patch('main.get_user_data')
@patch('main.get_user_repos')
def test_get_user_endpoint_partial(mock_repos, mock_user):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"login": "testuser", "followers": 5}
    mock_user.return_value = mock_response
    # Return true for is_partial
    mock_repos.return_value = ([], True)
    
    response = client.get("/api/user?username=testuser")
    assert response.status_code == 200
    assert response.json()["is_partial"] is True

def test_get_user_not_found():
    mock_response = MagicMock()
    mock_response.status_code = 404
    with patch('main.get_user_data', return_value=mock_response):
        response = client.get("/api/user?username=nonexistent")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

def test_get_user_rate_limited():
    mock_response = MagicMock()
    mock_response.status_code = 403
    with patch('main.get_user_data', return_value=mock_response):
        response = client.get("/api/user?username=anyuser")
        assert response.status_code == 403
        assert "rate limit exceeded" in response.json()["detail"].lower()
