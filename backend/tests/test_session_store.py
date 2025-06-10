import pytest
from llms._session_store import DEFAULT_SESSION_STORE


@pytest.fixture
def session_store():
    return DEFAULT_SESSION_STORE()


def test_session_store_set_get():
    """Test setting and getting session data"""
    store = session_store()
    session_id = "test-session"
    data = "test-data"

    # Test setting data
    store.set(session_id, data)

    # Test getting data
    retrieved_data = store.get(session_id)
    assert retrieved_data == data


def test_session_store_get_nonexistent():
    """Test getting data for non-existent session"""
    store = session_store()
    retrieved_data = store.get("nonexistent-session")
    assert retrieved_data is None


def test_session_store_multiple_sessions():
    """Test handling multiple sessions"""
    store = session_store()
    session1 = "session1"
    session2 = "session2"
    data1 = "data1"
    data2 = "data2"

    # Set data for multiple sessions
    store.set(session1, data1)
    store.set(session2, data2)

    # Verify data is stored correctly
    assert store.get(session1) == data1
    assert store.get(session2) == data2
