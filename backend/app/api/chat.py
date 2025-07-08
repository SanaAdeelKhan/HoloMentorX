# app/api/chat.py
from fastapi import APIRouter
from app.schemas import ChatRequest, ChatResponse
import os
import httpx

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_llama(request: ChatRequest):
    message = request.message.strip()
    contract = request.contract.strip() if request.contract else ""

    prompt = [
        {"role": "system", "content": "You are a smart contract expert. Use the contract context to answer user questions."},
        {"role": "user", "content": f"Contract:\n{contract}"},
        {"role": "user", "content": message}
    ]

    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        return {"answer": "❌ GROQ_API_KEY is missing in environment variables."}

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {groq_key}"},
                json={
                    "model": "meta-llama/llama-4-scout-17b-16e-instruct",
                    "messages": prompt,
                    "temperature": 0.7,
                    "max_tokens": 500
                }
            )
        if response.status_code == 200:
            content = response.json()["choices"][0]["message"]["content"]
            return {"answer": content.strip()}
        else:
            return {"answer": f"❌ LLaMA response failed: {response.status_code}"}
    except Exception as e:
        return {"answer": f"❌ Error during chat: {str(e)}"}
