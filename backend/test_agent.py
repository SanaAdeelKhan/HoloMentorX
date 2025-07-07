import os
import traceback
import httpx
import multiprocessing
from dotenv import load_dotenv
from uagents import Agent, Context, Model
from typing import List

# ✅ Safe multiprocessing for Windows
try:
    multiprocessing.set_start_method("spawn")
except RuntimeError:
    pass

# ✅ Load environment variables
load_dotenv()

# ✅ Input model
class Message(Model):
    message: str

# ✅ Output model
class TestResponse(Model):
    test_cases: List[str]

# ✅ Define the test agent
test_agent = Agent(
    name="test_agent",
    seed="test-agent fixed seed phrase",
    port=8004,
    endpoint=["http://localhost:8004/submit"]
)

@test_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"🧪 test_agent ready at {ctx.agent.address}")

@test_agent.on_message(model=Message)
async def generate_tests(ctx: Context, sender: str, msg: Message):
    contract_code = msg.message.strip()

    prompt = f"""You are a test case generator for Qubic smart contracts.

Generate meaningful test cases for the following contract:

- ✅ What to test
- ⚠️ Edge cases
- 🧪 Performance concerns

Contract:
```cpp
{contract_code}
```"""

    asi_key = os.getenv("ASI_API_KEY")
    if not asi_key:
        await ctx.send(sender, TestResponse(test_cases=["❌ Missing ASI_API_KEY in .env"]))
        return

    try:
        ctx.logger.info("🧠 Calling ASI:One Mini for test generation...")
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.asi.one/v1/chat/completions",
                headers={"Authorization": f"Bearer {asi_key}"},
                json={
                    "model": "asi/one-mini",
                    "messages": [
                        {"role": "system", "content": "You are a test case generator for smart contracts."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.5,
                    "max_tokens": 800
                }
            )

        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            await ctx.send(sender, TestResponse(test_cases=[content.strip()]))
            ctx.logger.info("✅ Test cases sent.")
        else:
            ctx.logger.error(f"❌ ASI error {response.status_code}: {response.text}")
            await ctx.send(sender, TestResponse(test_cases=["❌ Failed to get test cases from ASI."]))
    except Exception as e:
        ctx.logger.error(f"❌ Exception: {e}\n{traceback.format_exc()}")
        await ctx.send(sender, TestResponse(test_cases=["❌ Internal error during test generation."]))
