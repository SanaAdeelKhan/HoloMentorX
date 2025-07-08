# backend/app/schemas.py

from pydantic import BaseModel
from typing import List

# 🔹 For Explain & General Message
class CodeRequest(BaseModel):
    code: str

class ContractInput(BaseModel):
    code: str  # Duplicate of CodeRequest, keep for flexibility

class Message(BaseModel):
    message: str

class ExplanationResponse(BaseModel):
    explanation: str

# 🔹 For Audit
class AuditResponse(BaseModel):
    issues: List[str]

# 🔹 For Chat

class ChatRequest(BaseModel):
    message: str
    contract: str = ""

class ChatResponse(BaseModel):
    answer: str
