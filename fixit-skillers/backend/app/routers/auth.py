from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Worker
from ..schemas import Register, Login, Token
from ..utils.security import hash_password, verify_password, create_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token)
def register(data: Register, db: Session = Depends(get_db)):
    if data.role not in ("CUSTOMER", "WORKER"):
        raise HTTPException(400, "Role must be CUSTOMER or WORKER")
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(409, "Email already registered")
    user = User(name=data.name, email=data.email, phone=data.phone,
                password_hash=hash_password(data.password), role=data.role, city=data.city)
    db.add(user)
    db.commit()
    db.refresh(user)
    if data.role == "WORKER":
        # Default to first category; worker can change it from profile later.
        from ..models import ServiceCategory
        category = db.query(ServiceCategory).first()
        if not category:
            category = ServiceCategory(name="Other Services", description="General services", icon="🛠️")
            db.add(category); db.commit(); db.refresh(category)
        worker = Worker(user_id=user.id, service_id=category.id, city=data.city or "Bengaluru")
        db.add(worker); db.commit()
    return {"access_token": create_token(user), "token_type": "bearer",
            "user": {"id": user.id, "name": user.name, "role": user.role}}

@router.post("/login", response_model=Token)
def login(data: Login, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Invalid email or password")
    return {"access_token": create_token(user), "token_type": "bearer",
            "user": {"id": user.id, "name": user.name, "role": user.role}}
