from fastapi import APIRouter, Depends
from ..utils.security import current_user
from ..models import User

router = APIRouter(prefix="/me", tags=["Profile"])

@router.get("")
def me(user: User = Depends(current_user)):
    return {"id": user.id, "name": user.name, "email": user.email, "phone": user.phone,
            "role": user.role, "city": user.city}
