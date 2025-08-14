from pydantic import BaseModel
from uuid import UUID
from src.product.schemas import ProductSearchSchema
from datetime import datetime

class InventoryReadSchema(BaseModel):
    sku: str
    product_name: str
    available_quantity: int
    reserved_quantity: int
