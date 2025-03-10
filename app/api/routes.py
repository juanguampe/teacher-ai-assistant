from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from app.models.chat import ChatMessage, ChatResponse
from app.utils.openai_utils import get_openai_response

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    user_id: Optional[str] = None

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint that connects to OpenAI Assistant API.
    
    This implementation uses the OpenAI Assistant API to:
    - Maintain conversation context within a thread
    - Access the assistant's pre-configured knowledge
    - Leverage the assistant's capabilities
    """
    try:
        # Use the conversation_id if provided, otherwise create a new one
        conversation_id = request.conversation_id or "new_conversation"
        
        # Pass both the message and conversation_id to maintain thread context
        response = await get_openai_response(
            message=request.message,
            conversation_id=conversation_id
        )
        
        # Create a response object
        chat_response = ChatResponse(
            message=response,
            conversation_id=conversation_id,
            success=True
        )
        
        return chat_response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat request: {str(e)}"
        )
