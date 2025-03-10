from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from pydantic import BaseModel
from typing import List, Optional
from app.models.chat import ChatMessage, ChatResponse
from app.utils.openai_utils import get_openai_response
from app.utils.document_loader import ingest_documents
import json
import os

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

@router.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    """Upload a JSON document to the application"""
    try:
        # Create documents directory if it doesn't exist
        os.makedirs("documents/json", exist_ok=True)
        
        # Read the uploaded file content
        content = await file.read()
        
        # Validate that it's valid JSON
        try:
            json.loads(content.decode('utf-8'))
        except json.JSONDecodeError:
            return {"success": False, "message": "Invalid JSON file"}
        
        # Save the file
        file_path = f"documents/json/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Ingest the document
        ingest_documents(
            documents_dir="documents/json",
            persist_dir="./chroma_db",
            chunk_size=1000,
            chunk_overlap=200
        )
        
        return {"success": True, "message": f"Document {file.filename} uploaded and ingested successfully"}
    except Exception as e:
        return {"success": False, "message": f"Error uploading document: {str(e)}"}
