from fastapi import APIRouter
from app.schemas import ContractInput
from app.ai import call_asi_one

router = APIRouter()

@router.post("/")
async def audit_contract(contract: ContractInput):
    prompt = f"""🔍 Please audit this Qubic smart contract. List:
- 🛡️ Security issues
- ❗ Vulnerabilities
- ✅ Best practices\n\nContract:\n{contract.code}"""
    result = call_asi_one(prompt)
    return {"issues": [result]}
