from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Worker, Booking, WorkerKYC
from ..utils.security import require_role

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/stats")
def stats(user=Depends(require_role("ADMIN")), db: Session = Depends(get_db)):
    return {
        "customers": db.query(User).filter(User.role=="CUSTOMER").count(),
        "workers": db.query(User).filter(User.role=="WORKER").count(),
        "verified_workers": db.query(Worker).filter(Worker.verified==True).count(),
        "pending_kyc": db.query(WorkerKYC).filter(WorkerKYC.status=="PENDING").count(),
        "bookings": db.query(Booking).count(),
        "completed": db.query(Booking).filter(Booking.status=="COMPLETED").count(),
    }

@router.get("/workers")
def workers(user=Depends(require_role("ADMIN")), db: Session = Depends(get_db)):
    return [{"id":w.id,"name":w.user.name,"email":w.user.email,"verified":w.verified,
             "service":w.service.name,"rating":w.rating,"jobs":w.completed_jobs} for w in db.query(Worker).all()]
