from uagents import Model

class ResponseMessage(Model):
    response_type: str  # e.g. "track", "explain", "audit"
    answer: str
