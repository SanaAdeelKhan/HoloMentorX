from fastapi import APIRouter
from app.schemas import ContractInput
from app.ai import call_asi_one

router = APIRouter()

@router.post("/")
async def test_contract(contract: ContractInput):
    prompt = f"""🧪 Test this Qubic smart contract. Describe:
- What tests should be run?
- What edge cases to cover?
- What results to expect?\n\nContract:\n{contract.code}"""
    result = call_asi_one(prompt)
    return {"test_results": result}
