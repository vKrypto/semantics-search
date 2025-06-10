import os
from unittest.mock import Mock, patch

import pytest
from llms.gpt import GPTGenerator


@pytest.fixture
def mock_openai_response():
    return {"choices": [{"message": {"content": "This is a test response"}}], "id": "test-id"}


@pytest.fixture
def gpt_generator():
    # Mock the API token for testing
    with patch.dict(os.environ, {"OPENAI_APIKEY": "test-token"}):
        return GPTGenerator(model_name="gpt-3.5-turbo", context="Test context")


def test_gpt_generator_initialization():
    """Test GPTGenerator initialization"""
    with patch.dict(os.environ, {"OPENAI_APIKEY": "test-token"}):
        generator = GPTGenerator(model_name="gpt-3.5-turbo", context="Test context")
        assert generator.model_name == "gpt-3.5-turbo"
        assert generator.context == "Test context"
        assert generator.session_id is not None


def test_gpt_generator_missing_api_key():
    """Test GPTGenerator initialization without API key"""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(EnvironmentError) as exc_info:
            GPTGenerator(model_name="gpt-3.5-turbo", context="Test context")
        assert "OPENAPI_KEY not found" in str(exc_info.value)


@patch("openai.OpenAI")
def test_get_response(mock_openai, gpt_generator, mock_openai_response):
    """Test get_response method"""
    # Mock the OpenAI client
    mock_client = Mock()
    mock_openai.return_value = mock_client
    mock_client.chat.completions.create.return_value = mock_openai_response

    # Test the response
    response = gpt_generator.get_response("Test query")

    assert response["response"] == "This is a test response"
    assert "timings" in response
    mock_client.chat.completions.create.assert_called_once()


def test_get_prompt_and_context(gpt_generator):
    """Test _get_prompt_and_context method"""
    # Test with no session context
    prompt, context = gpt_generator._get_prompt_and_context("Test query")
    assert "Test context" in prompt
    assert "Test query" in prompt
    assert context is None

    # Test with session context
    gpt_generator._session_store.set(gpt_generator.session_id, "test-context")
    prompt, context = gpt_generator._get_prompt_and_context("Test query")
    assert context == "test-context"
