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

from uagents import Agent, Context, Model

class Message(Model):
    message: str

explain_agent = Agent(
    name="explain_agent",
    seed="explain-agent fixed seed",
    port=8001,
    endpoint=["http://localhost:8001/submit"]
)

@explain_agent.on_event("startup")
async def startup_explain(ctx: Context):
    ctx.logger.info(f"📘 explain_agent address: {ctx.agent.address}")

@explain_agent.on_message(model=Message)
async def explain_contract(ctx: Context, sender: str, msg: Message):
    contract_code = msg.message.strip()
    prompt = f"""You are an expert in Qubic smart contracts.

Please explain the following contract in clear and simple language, section by section.

Qubic Contract:
```cpp
{msg.message}
```"""
    await ctx.send(sender, {"message": explanation})

    try:
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key:
            ctx.logger.info("🤖 Calling Groq for explanation")
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {groq_key}"},
                    json={
                        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
                        "messages": [
                            {"role": "system", "content": "You are a smart contract explainer."},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.5,
                        "max_tokens": 600
                    }
                )
            if response.status_code == 200:
                content = response.json()["choices"][0]["message"]["content"]
                await ctx.send(sender, Message(message=content.strip()))
                ctx.logger.info("✅ Explanation sent.")
            else:
                await ctx.send(sender, Message(message="❌ Failed to fetch explanation."))
        else:
            ctx.logger.warning("⚠️ GROQ_API_KEY is missing.")
            await ctx.send(sender, Message(message="⚠️ GROQ_API_KEY not found."))
    except Exception as e:
        ctx.logger.error(f"❌ explain_agent error: {e}\n{traceback.format_exc()}")
        await ctx.send(sender, Message(message="❌ Internal error during explanation."))
