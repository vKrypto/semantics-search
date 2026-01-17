"""Utility for managing conversation history in Redis.

This module provides shared functionality for loading and saving conversation
history across different LLM providers. It follows the project's architecture
by keeping infrastructure concerns in the core/utils layer.
"""
import json
from typing import Dict, List, Optional, Any

from core.config.settings import AppSettings
from core.logging.logger import logger
from core.utils.redis_client import get_redis_client


def get_conversation_history_key(provider_name: str, session_id: str) -> str:
    """Get the Redis key for a session's conversation history.
    
    Args:
        provider_name: The LLM provider name (e.g., 'openai', 'cohere')
        session_id: The session ID
        
    Returns:
        Redis key string
    """
    return f"{AppSettings.REDIS_CHAT_HISTORY_PREFIX}{provider_name}:{session_id}"


def load_conversation_history(provider_name: str, session_id: str) -> List[Dict[str, str]]:
    """Load conversation history from Redis.
    
    Args:
        provider_name: The LLM provider name
        session_id: The session ID
        
    Returns:
        List of message dictionaries with role and content
    """
    client = get_redis_client()
    if client is None:
        return []
    
    try:
        redis_key = get_conversation_history_key(provider_name, session_id)
        raw = client.get(redis_key)
        if not raw:
            return []
        
        parsed: Any = json.loads(raw)
        if not isinstance(parsed, list):
            return []
        
        # Keep only well-formed messages
        cleaned: List[Dict[str, str]] = []
        for m in parsed:
            if not isinstance(m, dict):
                continue
            role = m.get("role")
            content = m.get("content")
            if isinstance(role, str) and isinstance(content, str):
                cleaned.append({"role": role, "content": content})
        return cleaned
    except Exception as e:
        logger.warning(f"Failed to load conversation history from Redis: {e}")
        return []


def save_conversation_history(
    provider_name: str, session_id: str, history: List[Dict[str, str]]
) -> None:
    """Save conversation history to Redis.
    
    Args:
        provider_name: The LLM provider name
        session_id: The session ID
        history: List of message dictionaries to save
    """
    client = get_redis_client()
    if client is None:
        return
    
    try:
        redis_key = get_conversation_history_key(provider_name, session_id)
        client.set(
            redis_key,
            json.dumps(history),
            ex=AppSettings.REDIS_CHAT_HISTORY_TTL_SECONDS,
        )
    except Exception as e:
        logger.warning(f"Failed to save conversation history to Redis: {e}")


def merge_with_history(
    history: List[Dict[str, str]], incoming: List[Dict[str, str]]
) -> List[Dict[str, str]]:
    """Merge history + incoming messages and ensure exactly one system message at the beginning.
    
    Args:
        history: Existing conversation history
        incoming: New messages to add
        
    Returns:
        Merged message list with exactly one system message at the start
    """
    combined = (history or []) + (incoming or [])

    system_msg = next((m for m in combined if m.get("role") == "system"), None)
    if not system_msg:
        system_msg = {"role": "system", "content": "You are a helpful AI assistant."}

    non_system = [
        {"role": m["role"], "content": m["content"]}
        for m in combined
        if isinstance(m, dict)
        and isinstance(m.get("role"), str)
        and isinstance(m.get("content"), str)
        and m.get("role") != "system"
    ]
    return [system_msg] + non_system
