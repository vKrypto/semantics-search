from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Message(BaseModel):
    """A chat message."""

    role: str = Field(..., description="The role of the message sender (user/assistant)")
    content: str = Field(..., description="The content of the message")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatSession(BaseModel):
    """A chat session containing multiple messages."""

    session_id: str = Field(..., description="Unique identifier for the chat session")
    messages: List[Message] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ChatRequest(BaseModel):
    """A chat request from the user."""

    query: str = Field(..., description="The user's query")
    session_id: Optional[str] = Field(None, description="Optional session ID for continuing a conversation")


class ChatResponse(BaseModel):
    """A chat response to the user."""

    response: str = Field(..., description="The assistant's response")
    context: Optional[List[str]] = Field(None, description="Context used to generate the response")
    server_time: float = Field(..., description="Server processing time in milliseconds")
    context_creation_time: Optional[float] = Field(None, description="Time taken to create context in milliseconds")
