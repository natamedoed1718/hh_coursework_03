import pytest
from unittest.mock import patch
from src.api_client import HHAPIClient

def test_get_employer():
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {"id": 1, "name": "Test"}
        client = HHAPIClient()
        result = client.get_employer(1)
        assert result["id"] == 1

