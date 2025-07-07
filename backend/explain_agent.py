from uagents import Agent, Context, Model
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

# ✅ Load environment variables
load_dotenv()

# ✅ Define the input/output message format
class Message(Model):
    message: str

# ✅ Initialize the agent on port 8001
explain_agent = Agent(
    name="explain_agent",
    seed="explain-agent fixed seed",
    port=8001,
    endpoint=["http://localhost:8001/submit"]
)

# ✅ Log startup
@explain_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"📘 explain_agent running at address: {ctx.agent.address}")

# ✅ Main logic using ASI:One mini
@explain_agent.on_message(model=Message)
async def handle_explanation(ctx: Context, sender: str, msg: Message):
    prompt = f"""You are an expert in Qubic smart contracts.

Please explain the following contract in clear and simple English:

Qubic Smart Contract:
```cpp
{msg.message}
```"""

    try:
        asi_api_key = os.getenv("ASI_API_KEY")
        if not asi_api_key:
            await ctx.send(sender, Message(message="⚠️ ASI_API_KEY not set in environment."))
            return

        ctx.logger.info("🤖 Calling ASI:One mini for contract explanation")

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.asi.one/v1/chat/completions",
                headers={"Authorization": f"Bearer {asi_api_key}"},
                json={
                    "model": "asi/one-mini",
                    "messages": [
                        {"role": "system", "content": "You are a smart contract explainer."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.5,
                    "max_tokens": 800
                }
            )

        if response.status_code == 200:
            content = response.json()["choices"][0]["message"]["content"]
            await ctx.send(sender, Message(message=content.strip()))
            ctx.logger.info("✅ Explanation sent back to user.")
        else:
            ctx.logger.error(f"❌ ASI API error {response.status_code}: {response.text}")
            await ctx.send(sender, Message(message="❌ Failed to get explanation from ASI."))
    except Exception as e:
        ctx.logger.error(f"❌ Exception: {e}\n{traceback.format_exc()}")
        await ctx.send(sender, Message(message="❌ Internal error during explanation."))
