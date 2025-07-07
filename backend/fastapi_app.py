import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

class ContractInput(BaseModel):
    message: str


# ✅ Initialize FastAPI app
app = FastAPI(
    title="HoloMentorX Smart Contract Agent API",
    description="API for interacting with HoloMentorX smart contract agents"
)

# ✅ Enable CORS for frontend (e.g., Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Reusable async HTTP function for agent calls
async def ask_agent_http(url: str, payload: dict):
    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        return response.json()

# ✅ Explain Contract Endpoint
@app.post("/explain")
async def explain_contract(contract: ContractInput):
    try:
        response = await ask_agent_http("http://localhost:8001/submit", {"message": contract.code})
        return {"explanation": response.get("message", "No explanation received.")}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# ✅ Audit Contract Endpoint
@app.post("/audit")
async def audit_contract(contract: ContractInput):
    try:
        response = await ask_agent_http("http://localhost:8003/submit", {"message": contract.code})
        return {"result": response.get("issues", ["No issues received."])}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# ✅ Test Contract Endpoint
@app.post("/test")
async def test_contract(contract: ContractInput):
    try:
        response = await ask_agent_http("http://localhost:8004/submit", {"message": contract.code})
        return {"result": response.get("test_cases", ["No test cases received."])}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
