# messages/shared.py

from uagents import Model
from typing import List

# Shared contract name constant (optional use)
CONTRACT_NAME = "TrackedContract"

# Message to send contract code
class Message(Model):
    message: str

# Response from audit agent
class AuditResponse(Model):
    issues: str

# Response from test agent
class TestResponse(Model):
    test_cases: List[str]
