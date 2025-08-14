import uuid

def generate_short_uuid() -> str:
    return uuid.uuid4().hex[:12].upper()
