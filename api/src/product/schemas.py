from pydantic import BaseModel
from uuid import UUID


class ProductItemSchema(BaseModel):
    id: UUID
    sku: str
    name: str
    price: float
    available_quantity: int


class ProductSearchSchema(BaseModel):
    items: list[ProductItemSchema]
    
    total: int
    page: int
    size: int
    pages: int
    
    
    