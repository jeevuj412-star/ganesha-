from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Worker, WorkerKYC, ServiceCategory, Notification
from ..schemas import KYCSubmit
from ..utils.security import current_user, require_role

router = APIRouter(prefix="/workers", tags=["Workers"])

def worker_out(w):
    return {
        "id": w.id, "user_id": w.user_id, "name": w.user.name, "email": w.user.email,
        "service": w.service.name, "bio": w.bio or "", "skills": w.skills or "",
        "experience_years": w.experience_years, "hourly_rate": w.hourly_rate,
        "city": w.city, "verified": w.verified, "available": w.available,
        "rating": w.rating, "completed_jobs": w.completed_jobs
    }

@router.get("")
def list_workers(service_id: int | None = None, city: str | None = None, db: Session = Depends(get_db)):
    q = db.query(Worker).join(User).filter(User.is_active == True)
    if service_id: q = q.filter(Worker.service_id == service_id)
    if city: q = q.filter(Worker.city.ilike(f"%{city}%"))
    return [worker_out(w) for w in q.limit(100).all()]

@router.get("/me")
def my_worker(user=Depends(require_role("WORKER")), db: Session = Depends(get_db)):
    w = db.query(Worker).filter(Worker.user_id == user.id).first()
    return worker_out(w)

@router.post("/kyc")
def submit_kyc(data: KYCSubmit, user=Depends(require_role("WORKER")), db: Session = Depends(get_db)):
    w = db.query(Worker).filter(Worker.user_id == user.id).first()
    if not w: raise HTTPException(404, "Worker profile not found")
    kyc = db.query(WorkerKYC).filter(WorkerKYC.worker_id == w.id).first()
    if not kyc:
        kyc = WorkerKYC(worker_id=w.id, **data.model_dump())
        db.add(kyc)
    else:
        for k,v in data.model_dump().items(): setattr(kyc, k, v)
        kyc.status = "PENDING"
    w.verified = False
    db.commit()
    return {"message": "KYC submitted for review", "status": kyc.status}

@router.get("/kyc")
def get_kyc(user=Depends(require_role("WORKER")), db: Session = Depends(get_db)):
    w = db.query(Worker).filter(Worker.user_id == user.id).first()
    return db.query(WorkerKYC).filter(WorkerKYC.worker_id == w.id).first()

@router.post("/availability")
def set_availability(available: bool, user=Depends(require_role("WORKER")), db: Session = Depends(get_db)):
    w = db.query(Worker).filter(Worker.user_id == user.id).first()
    w.available = available
    db.commit()
    return {"available": available}

@router.get("/admin/kyc")
def admin_kyc(user=Depends(require_role("ADMIN")), db: Session = Depends(get_db)):
    rows = db.query(WorkerKYC).all()
    return [{
        "id": k.id, "worker_id": k.worker_id, "worker_name": k.worker.user.name,
        "legal_name": k.legal_name, "address": k.address, "status": k.status,
        "aadhaar_last4": k.aadhaar_last4, "pan_masked": k.pan_masked
    } for k in rows]

@router.post("/admin/kyc/{kyc_id}/decision")
def kyc_decision(kyc_id: int, status: str, reason: str = "", user=Depends(require_role("ADMIN")), db: Session = Depends(get_db)):
    if status not in ("VERIFIED", "REJECTED"):
        raise HTTPException(400, "Status must be VERIFIED or REJECTED")
    k = db.get(WorkerKYC, kyc_id)
    if not k: raise HTTPException(404, "KYC not found")
    k.status = status
    k.rejection_reason = reason
    k.worker.verified = status == "VERIFIED"
    db.add(Notification(user_id=k.worker.user_id, title="KYC Update",
                        message=f"Your KYC status is {status}."))
    db.commit()
    return {"message": status}
