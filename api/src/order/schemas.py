from typing import List, Optional, Annotated
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime



class OrderItemSchema(BaseModel):
    sku: str
    quantity: Annotated[int, Field(strict=True, gt=0)]

class CustomerSchema(BaseModel):
    user_id: str
    email: EmailStr

class OrderCreateSchema(BaseModel):
    customer: CustomerSchema
    items: List[OrderItemSchema]
    
class OrderReadSchema(BaseModel):
    order_id: str
    status: str
    message: str
    estimated_total: float
    created_at: datetime
    
class PricingSchema(BaseModel):
    subtotal: float
    tax: float
    total: float

class PaymentSchema(BaseModel):
    status: str
    transaction_id: Optional[str]
    
class OrderReadByIdSchema(BaseModel):
    order_id: str = Field(..., description="Custom formatted order ID")
    status: str
    customer: CustomerSchema
    items: List[OrderItemSchema]
    pricing: PricingSchema
    payment: PaymentSchema
    created_at: datetime
    updated_at: datetime
    
class OrderUserItemSearchSchema(BaseModel):
    order_id: str
    status: str
    total: float
    created_at: str
    

class OrdersUserSearchSchema(BaseModel):
    items: List[OrderUserItemSearchSchema]
    
    total: int
    page: int
    size: int
    pages: int
