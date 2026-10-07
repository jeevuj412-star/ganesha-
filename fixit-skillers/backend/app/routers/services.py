from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import ServiceCategory
from ..schemas import ServiceOut
from ..utils.security import require_role

router = APIRouter(prefix="/services", tags=["Services"])

@router.get("", response_model=list[ServiceOut])
def list_services(db: Session = Depends(get_db)):
    return db.query(ServiceCategory).filter(ServiceCategory.active == True).order_by(ServiceCategory.name).all()

@router.post("", dependencies=[Depends(require_role("ADMIN"))])
def create_service(name: str, description: str = "", icon: str = "🛠️", db: Session = Depends(get_db)):
    s = ServiceCategory(name=name, description=description, icon=icon)
    db.add(s); db.commit(); db.refresh(s)
    return s
