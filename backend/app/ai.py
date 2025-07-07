# app/ai.py

import os
import openai

# ✅ Load ASI API Key from environment
ASI_API_KEY = os.getenv("ASI_API_KEY")
if not ASI_API_KEY:
    raise ValueError("❌ ASI_API_KEY is missing in environment variables.")

# ✅ Set OpenAI-compatible ASI endpoint
openai.api_key = ASI_API_KEY
openai.api_base = "https://api.asi1.ai/v1"  # ✅ correct endpoint

# ✅ Core function to call asi1-mini model
def call_asi_one(prompt: str, model: str = "asi1-mini") -> str:
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a smart contract expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ ASI error: {str(e)}"
