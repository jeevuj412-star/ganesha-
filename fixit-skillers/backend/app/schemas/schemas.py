from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class Register(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    password: str
    city: Optional[str] = "Bengaluru"
    role: str

class Login(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

class ServiceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str
    icon: str

class WorkerOut(BaseModel):
    id: int
    user_id: int
    name: str
    email: str
    service: str
    bio: str
    skills: str
    experience_years: int
    hourly_rate: float
    city: str
    verified: bool
    available: bool
    rating: float
    completed_jobs: int

class BookingCreate(BaseModel):
    worker_id: int
    service_id: int
    address: str
    scheduled_at: datetime
    description: str = ""
    budget: float = 0

class BookingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    customer_id: int
    worker_id: int
    service_id: int
    address: str
    scheduled_at: datetime
    description: str
    budget: float
    status: str

class KYCSubmit(BaseModel):
    legal_name: str
    dob: Optional[str] = None
    address: str
    aadhaar_last4: Optional[str] = None
    pan_masked: Optional[str] = None

class ReviewCreate(BaseModel):
    booking_id: int
    rating: int
    comment: str = ""
