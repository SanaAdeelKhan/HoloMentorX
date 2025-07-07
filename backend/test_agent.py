import os
import html
import traceback
import httpx
import multiprocessing
from dotenv import load_dotenv
from uagents import Agent, Context, Model
from typing import List

# ✅ Ensure proper multiprocessing on Windows
try:
    multiprocessing.set_start_method("spawn")
except RuntimeError:
    pass

# ✅ Load environment variables
load_dotenv()

# ✅ Input message model
class Message(Model):
    message: str

# ✅ Response model (shared with FastAPI)
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
    ctx.logger.info(f"🧪 test_agent address: {ctx.agent.address}")

@test_agent.on_message(model=Message)
async def generate_tests(ctx: Context, sender: str, msg: Message):
    contract_code = msg.message.strip()
    ctx.logger.info(f"📥 Received contract for test generation:\n{contract_code}")

    prompt = f"""
You are a smart contract test case generator specialized in **Qubic C++-style contracts**.

Please generate test cases for the following Qubic smart contract.

Each test case should help ensure that core contract functions work correctly, handle edge cases, and fail safely if misused.

Your response MUST be in markdown with:
- ✅ What to test
- ⚠️ Edge cases to consider
- 🧪 Any performance or resource constraints

Qubic Contract:
```cpp
{contract_code}

"""

    groq_key = os.getenv("GROQ_API_KEY")
    asi_key = os.getenv("ASI_API_KEY")
    test_lists = []

    # 🔹 Groq
    if groq_key:
        try:
            ctx.logger.info("🤖 Calling Groq")
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {groq_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
                        "messages": [
                            {"role": "system", "content": "You are a smart contract test case generator."},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.5,
                        "max_tokens": 600
                    }
                )
            res_json = response.json()
            if response.status_code == 200 and "choices" in res_json:
                content = res_json["choices"][0]["message"]["content"]
                lines = content.strip().splitlines()
                test_lists.append(f"## 🤖 Groq\n" + "\n".join(lines))
            else:
                test_lists.append("## 🤖 Groq\n❌ Failed to fetch test cases.")
        except Exception as e:
            ctx.logger.error(f"❌ Groq Exception: {e}\n{traceback.format_exc()}")
            test_lists.append("## 🤖 Groq\n❌ Internal error.")
    else:
        ctx.logger.warning("⚠️ GROQ_API_KEY is missing.")

    # 🔹 ASI1
    if asi_key:
        try:
            ctx.logger.info("🧠 Calling ASI1")
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.asi1.ai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {asi_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "asi1-mini",
                        "messages": [
                            {"role": "system", "content": "You are a Solidity test case generator."},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.5,
                        "max_tokens": 600
                    }
                )
            res_json = response.json()
            if response.status_code == 200 and "choices" in res_json:
                content = res_json["choices"][0]["message"]["content"]
                lines = content.strip().splitlines()
                test_lists.append(f"## 🧠 ASI1\n" + "\n".join(lines))
            else:
                test_lists.append("## 🧠 ASI1\n❌ Failed to fetch test cases.")
        except Exception as e:
            ctx.logger.error(f"❌ ASI1 Exception: {e}\n{traceback.format_exc()}")
            test_lists.append("## 🧠 ASI1\n❌ Internal error.")
    else:
        ctx.logger.warning("⚠️ ASI_API_KEY is missing.")

    # 🔹 Combine and respond
    if test_lists:
        combined = "\n\n---\n\n".join(test_lists)
        await ctx.send(sender, TestResponse(test_cases=[combined]))
        ctx.logger.info("✅ Sent combined test scenarios.")
    else:
        await ctx.send(sender, TestResponse(test_cases=["❌ No test cases generated."]))
        ctx.logger.error("❌ Failed to generate test cases.")
