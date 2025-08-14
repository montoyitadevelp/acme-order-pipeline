import uuid
import hashlib

def generate_short_uuid() -> str:
    return uuid.uuid4().hex[:12].upper()

def generate_order_hash(customer: dict, items: list[dict]) -> str:
        """
        Generate a deterministic hash for idempotency check.
        Based on user_id and items list.
        """
        items_str = "|".join([f"{i['sku']}:{i['quantity']}" for i in sorted(items, key=lambda x: x['sku'])])
        raw_string = f"{customer['user_id']}|{items_str}"
        return hashlib.sha256(raw_string.encode("utf-8")).hexdigest()
