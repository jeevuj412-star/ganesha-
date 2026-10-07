from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Booking, Worker, Notification
from ..schemas import BookingCreate, BookingOut
from ..utils.security import require_role

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("", response_model=BookingOut)
def create_booking(data: BookingCreate, user=Depends(require_role("CUSTOMER")), db: Session = Depends(get_db)):
    worker = db.get(Worker, data.worker_id)
    if not worker or not worker.available:
        raise HTTPException(400, "Worker is unavailable")
    conflict = db.query(Booking).filter(
        Booking.worker_id == data.worker_id,
        Booking.scheduled_at == data.scheduled_at,
        Booking.status.in_(["PENDING","ACCEPTED","IN_PROGRESS"])
    ).first()
    if conflict:
        raise HTTPException(409, "Worker already has a booking at this time")
    booking = Booking(customer_id=user.id, **data.model_dump())
    db.add(booking)
    db.flush()
    db.add(Notification(user_id=worker.user_id, title="New Booking",
                        message=f"New service booking #{booking.id}"))
    db.commit(); db.refresh(booking)
    return booking

@router.get("/mine", response_model=list[BookingOut])
def my_bookings(user=Depends(require_role("CUSTOMER")), db: Session = Depends(get_db)):
    return db.query(Booking).filter(Booking.customer_id == user.id).order_by(Booking.created_at.desc()).all()

@router.get("/worker", response_model=list[BookingOut])
def worker_bookings(user=Depends(require_role("WORKER")), db: Session = Depends(get_db)):
    w = db.query(Worker).filter(Worker.user_id == user.id).first()
    return db.query(Booking).filter(Booking.worker_id == w.id).order_by(Booking.created_at.desc()).all()

def change_status(booking_id, status, user, db):
    b = db.get(Booking, booking_id)
    if not b: raise HTTPException(404, "Booking not found")
    w = db.query(Worker).filter(Worker.user_id == user.id).first()
    if not w or b.worker_id != w.id: raise HTTPException(403, "Not your booking")
    b.status = status
    if status == "COMPLETED":
        w.completed_jobs += 1
    db.add(Notification(user_id=b.customer_id, title="Booking Update",
                        message=f"Booking #{b.id} is now {status}."))
    db.commit(); db.refresh(b)
    return b

@router.post("/{booking_id}/accept", response_model=BookingOut)
def accept(booking_id: int, user=Depends(require_role("WORKER")), db: Session = Depends(get_db)):
    return change_status(booking_id, "ACCEPTED", user, db)

@router.post("/{booking_id}/reject", response_model=BookingOut)
def reject(booking_id: int, user=Depends(require_role("WORKER")), db: Session = Depends(get_db)):
    return change_status(booking_id, "REJECTED", user, db)

@router.post("/{booking_id}/start", response_model=BookingOut)
def start(booking_id: int, user=Depends(require_role("WORKER")), db: Session = Depends(get_db)):
    return change_status(booking_id, "IN_PROGRESS", user, db)

@router.post("/{booking_id}/complete", response_model=BookingOut)
def complete(booking_id: int, user=Depends(require_role("WORKER")), db: Session = Depends(get_db)):
    return change_status(booking_id, "COMPLETED", user, db)

@router.post("/{booking_id}/cancel", response_model=BookingOut)
def cancel(booking_id: int, user=Depends(require_role("CUSTOMER")), db: Session = Depends(get_db)):
    b = db.get(Booking, booking_id)
    if not b or b.customer_id != user.id: raise HTTPException(404, "Booking not found")
    if b.status in ("COMPLETED","CANCELLED"): raise HTTPException(400, "Booking cannot be cancelled")
    b.status = "CANCELLED"
    db.add(Notification(user_id=b.worker.user_id, title="Booking Cancelled", message=f"Booking #{b.id} was cancelled."))
    db.commit(); db.refresh(b)
    return b
