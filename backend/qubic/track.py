# qubic/track.py

import json
import os
from datetime import datetime

TRACK_DB_PATH = "qubic/tracked_contracts.json"

# 🔧 Ensure tracking folder exists
os.makedirs("qubic", exist_ok=True)

def extract_metadata(contract_code: str) -> dict:
    lines = contract_code.splitlines()
    functions = [line.strip() for line in lines if line.strip().startswith("function")]
    metadata = {
        "timestamp": datetime.utcnow().isoformat(),
        "function_count": len(functions),
        "functions": functions,
        "line_count": len(lines),
    }
    return metadata

def track_contract(contract_code: str, contract_name: str = "UnnamedContract") -> dict:
    metadata = extract_metadata(contract_code)
    metadata["contract_name"] = contract_name

    # Load existing tracking log
    if os.path.exists(TRACK_DB_PATH):
        with open(TRACK_DB_PATH, "r") as f:
            tracked_contracts = json.load(f)
    else:
        tracked_contracts = {}

    # Save/update contract
    tracked_contracts[contract_name] = metadata

    with open(TRACK_DB_PATH, "w") as f:
        json.dump(tracked_contracts, f, indent=4)

    return metadata
