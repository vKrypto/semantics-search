from unittest.mock import Mock, patch

import pytest


def test_sample_function():
    """Test sample function to demonstrate pytest features."""
    # Arrange
    expected = True

    # Act
    actual = True

    # Assert
    assert actual == expected


@pytest.fixture
def mock_data():
    """Fixture to provide mock data for tests."""
    return {"id": 1, "title": "Test Document", "description": "This is a test document", "vectors": [0.1, 0.2, 0.3]}


def test_with_fixture(mock_data):
    """Test using the mock_data fixture."""
    assert mock_data["id"] == 1
    assert isinstance(mock_data["vectors"], list)
    assert len(mock_data["vectors"]) == 3


@pytest.mark.parametrize(
    "input_value,expected",
    [
        (1, True),
        (0, False),
        (-1, False),
    ],
)
def test_parameterized(input_value, expected):
    """Demonstrate parameterized testing."""
    result = input_value > 0
    assert result == expected


@patch("your_module.some_function")
def test_with_mock(mock_function):
    """Demonstrate mocking."""
    # Configure mock
    mock_function.return_value = "mocked result"

    # Use mock
    result = mock_function()

    # Assert
    assert result == "mocked result"
    mock_function.assert_called_once()
