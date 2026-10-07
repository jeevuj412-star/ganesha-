from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Booking, Review, Worker
from ..schemas import ReviewCreate
from ..utils.security import require_role

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("")
def create_review(data: ReviewCreate, user=Depends(require_role("CUSTOMER")), db: Session = Depends(get_db)):
    b = db.get(Booking, data.booking_id)
    if not b or b.customer_id != user.id: raise HTTPException(404, "Booking not found")
    if b.status != "COMPLETED": raise HTTPException(400, "Only completed bookings can be reviewed")
    if not 1 <= data.rating <= 5: raise HTTPException(400, "Rating must be 1-5")
    if db.query(Review).filter(Review.booking_id == b.id).first():
        raise HTTPException(409, "Already reviewed")
    r = Review(booking_id=b.id, customer_id=user.id, worker_id=b.worker_id,
               rating=data.rating, comment=data.comment)
    db.add(r)
    db.flush()
    w = db.get(Worker, b.worker_id)
    reviews = db.query(Review).filter(Review.worker_id == w.id).all()
    w.rating = sum(x.rating for x in reviews) / len(reviews)
    db.commit()
    return {"message": "Review submitted", "rating": w.rating}
