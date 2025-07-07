# backend/app/schemas.py
from pydantic import BaseModel

class CodeRequest(BaseModel):
    code: str

class ExplanationResponse(BaseModel):
    explanation: str

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str
