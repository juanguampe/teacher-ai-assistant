from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import uuid4

class ChatMessage(BaseModel):
    """Model for a chat message"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    conversation_id: str
    user_id: Optional[str] = None
    content: str
    role: str  # 'user' or 'assistant'
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        from_attributes = True  # Updated from orm_mode for Pydantic V2

class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    message: str
    conversation_id: str
    success: bool
    timestamp: datetime = Field(default_factory=datetime.now)
