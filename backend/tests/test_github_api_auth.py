import pytest
from unittest.mock import patch, MagicMock
import github_api

def test_get_headers_auth_enabled():
    """Test that Authorization header is present when enabled."""
    with patch('github_api.GITHUB_TOKEN', 'fake-token'), \
         patch('github_api.AUTH_ENABLED', True):
        headers = github_api.get_headers()
        assert "Authorization" in headers
        assert headers["Authorization"] == "token fake-token"

def test_get_headers_auth_disabled():
    """Test that Authorization header is absent when disabled."""
    with patch('github_api.GITHUB_TOKEN', 'fake-token'), \
         patch('github_api.AUTH_ENABLED', False):
        headers = github_api.get_headers()
        assert "Authorization" not in headers

def test_get_headers_no_token():
    """Test that Authorization header is absent when no token is present."""
    with patch('github_api.GITHUB_TOKEN', None), \
         patch('github_api.AUTH_ENABLED', True):
        headers = github_api.get_headers()
        assert "Authorization" not in headers

@patch('requests.get')
def test_api_calls_use_auth_header_when_enabled(mock_get):
    """Verify that actual API calls use headers from get_headers()."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    mock_get.return_value = mock_response
    
    with patch('github_api.GITHUB_TOKEN', 'fake-token'), \
         patch('github_api.AUTH_ENABLED', True):
        github_api.get_user_data("testuser")
        
        args, kwargs = mock_get.call_args
        headers = kwargs.get('headers')
        assert headers["Authorization"] == "token fake-token"

@patch('requests.get')
def test_api_calls_exclude_auth_header_when_disabled(mock_get):
    """Verify that actual API calls EXCLUDE Authorization when disabled."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    mock_get.return_value = mock_response
    
    with patch('github_api.GITHUB_TOKEN', 'fake-token'), \
         patch('github_api.AUTH_ENABLED', False):
        github_api.get_user_data("testuser")
        
        args, kwargs = mock_get.call_args
        headers = kwargs.get('headers')
        assert "Authorization" not in headers
