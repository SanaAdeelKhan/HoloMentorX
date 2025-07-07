from uagents import Agent, Context
from dotenv import load_dotenv
import os
import httpx
import traceback
from typing import List
import multiprocessing

# ✅ Safe multiprocessing for Windows
try:
    multiprocessing.set_start_method("spawn")
except RuntimeError:
    pass

# ✅ Load env vars
load_dotenv()

from messages.shared import Message, AuditResponse  # ✅ Ensure Message is also imported

# ✅ Define audit agent
audit_agent = Agent(
    name="audit_agent",
    seed="audit-agent fixed seed",
    port=8003,
    endpoint=["http://localhost:8003/submit"]
)

@audit_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"🔍 audit_agent address: {ctx.agent.address}")

@audit_agent.on_message(model=Message)
async def audit_contract(ctx: Context, sender: str, msg: Message):
    contract_code = msg.message.strip()
    ctx.logger.info(f"📥 Received contract to audit from {sender}:\n{contract_code}")

    prompt = f"""You are a security auditor for Qubic smart contracts.

Please audit this contract and list:
- 🛡️ Security issues
- ❗ Vulnerabilities
- ✅ Best practices

Qubic Contract:
```cpp
{contract_code}
```"""

    results = []
    groq_key = os.getenv("GROQ_API_KEY")
    asi_key = os.getenv("ASI_API_KEY")

    # 🔹 Groq
    if groq_key:
        try:
            ctx.logger.info("🤖 Calling Groq")
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {groq_key}"},
                    json={
                        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
                        "messages": [
                            {"role": "system", "content": "You are a smart contract auditor."},
                            {"role": "user", "content": prompt}
                        ]
                    }
                )
            if response.status_code == 200:
                content = response.json()["choices"][0]["message"]["content"]
                results.append("## 🤖 Groq\n" + content.strip())
            else:
                results.append("## 🤖 Groq\n❌ Failed to audit.")
        except Exception as e:
            ctx.logger.error(f"[GROQ Error] {e}\n{traceback.format_exc()}")
            results.append("## 🤖 Groq\n❌ Internal error.")
    else:
        ctx.logger.warning("⚠️ GROQ_API_KEY is missing.")

    # 🔹 ASI:One Mini
    if asi_key:
        try:
            ctx.logger.info("🧠 Calling ASI1")
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.asi1.ai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {asi_key}"},
                    json={
                        "model": "asi1-mini",
                        "messages": [
                            {"role": "system", "content": "You are a smart contract auditor."},
                            {"role": "user", "content": prompt}
                        ]
                    }
                )
            if response.status_code == 200:
                content = response.json()["choices"][0]["message"]["content"]
                results.append("## 🧠 ASI:One Mini\n" + content.strip())
            else:
                results.append("## 🧠 ASI:One Mini\n❌ Failed to audit.")
        except Exception as e:
            ctx.logger.error(f"[ASI1 Error] {e}\n{traceback.format_exc()}")
            results.append("## 🧠 ASI:One Mini\n❌ Internal error.")
    else:
        ctx.logger.warning("⚠️ ASI_API_KEY is missing.")

    # ✅ Final reply
    final = "\n\n---\n\n".join(results) if results else "❌ No results."
    await ctx.send(sender, AuditResponse(issues=[final]))
    ctx.logger.info("✅ Audit report sent.")
