# backend/app/api/chat.py
from fastapi import APIRouter
from app.schemas import ChatRequest, ChatResponse

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(body: ChatRequest):
    msg = body.message
    # TODO: integrate chat logic / memory
    answer = f"You said: {msg}. (Chatbot response)"
    return ChatResponse(answer=answer)
