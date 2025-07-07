from uagents import Agent, Context
from dotenv import load_dotenv
import os
import httpx
import traceback
import multiprocessing

# ✅ Safe multiprocessing for Windows
try:
    multiprocessing.set_start_method("spawn")
except RuntimeError:
    pass

load_dotenv()

from messages.shared import Message, AuditResponse  # ✅ Defined elsewhere

# ✅ Audit agent setup
audit_agent = Agent(
    name="audit_agent",
    seed="audit-agent fixed seed",
    port=8003,
    endpoint=["http://localhost:8003/submit"]
)

@audit_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"🛡️ audit_agent running at {ctx.agent.address}")

@audit_agent.on_message(model=Message)
async def handle_audit(ctx: Context, sender: str, msg: Message):
    contract_code = msg.message.strip()

    prompt = f"""You are a security auditor for Qubic smart contracts.

Please analyze this contract and report:
- 🔐 Security Issues
- 🐞 Vulnerabilities
- ✅ Best Practices

Contract:
```cpp
{contract_code}
```"""

    asi_key = os.getenv("ASI_API_KEY")

    if not asi_key:
        await ctx.send(sender, AuditResponse(issues=["❌ Missing ASI_API_KEY in environment."]))
        return

    try:
        ctx.logger.info("🧠 Calling ASI:One mini for audit...")
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.asi.one/v1/chat/completions",
                headers={"Authorization": f"Bearer {asi_key}"},
                json={
                    "model": "asi/one-mini",
                    "messages": [
                        {"role": "system", "content": "You are a smart contract auditor."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.5,
                    "max_tokens": 1000
                }
            )

        if response.status_code == 200:
            content = response.json()["choices"][0]["message"]["content"]
            ctx.logger.info("✅ Audit complete.")
            await ctx.send(sender, AuditResponse(issues=[content.strip()]))
        else:
            ctx.logger.error(f"❌ ASI Error {response.status_code}: {response.text}")
            await ctx.send(sender, AuditResponse(issues=["❌ Failed to audit contract via ASI."]))
    except Exception as e:
        ctx.logger.error(f"❌ Exception: {e}\n{traceback.format_exc()}")
        await ctx.send(sender, AuditResponse(issues=["❌ Internal error during audit."]))
