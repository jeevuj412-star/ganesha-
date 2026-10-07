from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine, SessionLocal
from .models import ServiceCategory, User
from .utils.security import hash_password
from .routers import auth, services, workers, bookings, reviews, admin, me

app = FastAPI(title="Fixit Skillers API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()
    categories = [
        ("Home Cleaning","Professional home and deep cleaning","🧹"),
        ("Electrician","Electrical installation and repairs","⚡"),
        ("Plumber","Plumbing and leakage repairs","🔧"),
        ("Carpenter","Furniture and woodwork","🪚"),
        ("Painter","Interior and exterior painting","🎨"),
        ("AC Repair","AC service and repair","❄️"),
        ("Appliance Repair","Repair home appliances","🔌"),
        ("Pest Control","Safe pest control services","🐜"),
        ("Beauty Services","At-home beauty and grooming","💇"),
        ("Mechanic","Vehicle repair and maintenance","🚗"),
        ("Computer Repair","Laptop and computer support","💻"),
        ("Gardening","Garden maintenance","🌱"),
    ]
    for name, desc, icon in categories:
        if not db.query(ServiceCategory).filter_by(name=name).first():
            db.add(ServiceCategory(name=name, description=desc, icon=icon))
    db.commit()
    admin_user = db.query(User).filter_by(email="admin@fixitskillers.local").first()
    if not admin_user:
        db.add(User(name="Fixit Admin", email="admin@fixitskillers.local",
                    password_hash=hash_password("Admin@123"), role="ADMIN", city="Bengaluru"))
        db.commit()
    db.close()

try:
    seed()
except Exception as exc:
    print("Seed skipped:", exc)

app.include_router(auth.router, prefix="/api")
app.include_router(services.router, prefix="/api")
app.include_router(workers.router, prefix="/api")
app.include_router(bookings.router, prefix="/api")
app.include_router(reviews.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(me.router, prefix="/api")

@app.get("/")
def root():
    return {"name":"Fixit Skillers API","status":"running"}
