# tick_utils.py

def get_mock_contract_state(tick: int) -> dict:
    return {
        "tick": tick,
        "balance": 1000 + tick,
        "status": "active" if tick % 2 == 0 else "inactive"
    }

# Example usage:
# print(get_mock_contract_state(42))
