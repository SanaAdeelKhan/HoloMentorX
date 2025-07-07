from fastapi import APIRouter
from app.schemas import ContractInput
import httpx, os

router = APIRouter()
import os
print("🔐 ASI_API_KEY loaded (starts with):", os.getenv("ASI_API_KEY")[:6], "...[hidden]")


ASI_API_KEY = os.getenv("ASI_API_KEY")
ASI_API_URL = "https://api.asi1.ai/v1/chat/completions"
MODEL_NAME = "asi1-mini"

@router.post("/")
async def explain_contract(contract: ContractInput):
    print("📥 Explain request received")
    if not ASI_API_KEY:
        return {"error": "❌ ASI_API_KEY missing from environment."}

    headers = {
        "Authorization": f"Bearer {ASI_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"Explain the following smart contract in simple terms:\n\n{contract.code}"

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(ASI_API_URL, json=payload, headers=headers)
            data = response.json()
            print("✅ ASI Response:", data)

            explanation = data["choices"][0]["message"]["content"]
            return {"explanation": explanation}

    except Exception as e:
        print("❌ ASI API Error:", e)
        return {"error": str(e)}
