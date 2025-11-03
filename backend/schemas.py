from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr

class PaymentCreate(BaseModel):
    amount: float
    currency: str = "usd"
    email: EmailStr
    name: str

class PaymentResponse(BaseModel):
    id: int
    amount: float
    currency: str
    status: str
    stripe_payment_intent: str
    created_at: datetime

    class Config:
        orm_mode = True
