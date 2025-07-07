import threading
import multiprocessing
import uvicorn
from fastapi_app import app
from audit_agent import audit_agent
from test_agent import test_agent
from explain_agent import explain_agent

# ✅ Ensure proper multiprocessing on Windows
try:
    multiprocessing.set_start_method("spawn", force=True)
except RuntimeError:
    pass

# 👇 Helper: run uAgent in its own thread with async loop
import asyncio

def start_agent(agent):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(agent.run_async())
    except Exception as e:
        print(f"❌ Agent '{agent.name}' failed: {e}")
    finally:
        loop.close()

# ✅ Main launcher
if __name__ == "__main__":
    threads = [
        threading.Thread(target=start_agent, args=(audit_agent,), daemon=False),
        threading.Thread(target=start_agent, args=(test_agent,), daemon=False),
        threading.Thread(target=start_agent, args=(explain_agent,), daemon=False),
        threading.Thread(target=lambda: uvicorn.run(app, host="0.0.0.0", port=8000), daemon=False)
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()
