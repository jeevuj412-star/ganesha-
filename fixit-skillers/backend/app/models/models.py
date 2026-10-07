from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(30), unique=True, nullable=True, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, index=True)
    city = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    worker = relationship("Worker", back_populates="user", uselist=False, cascade="all, delete-orphan")
    bookings_as_customer = relationship("Booking", foreign_keys="Booking.customer_id", back_populates="customer")
    bookings_as_worker = relationship("Booking", foreign_keys="Booking.worker_id", back_populates="worker_user")

class ServiceCategory(Base):
    __tablename__ = "service_categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True, nullable=False)
    description = Column(Text, default="")
    icon = Column(String(20), default="🛠️")
    active = Column(Boolean, default=True)
    workers = relationship("Worker", back_populates="service")

class Worker(Base):
    __tablename__ = "workers"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    service_id = Column(Integer, ForeignKey("service_categories.id"), nullable=False)
    bio = Column(Text, default="")
    skills = Column(Text, default="")
    experience_years = Column(Integer, default=0)
    hourly_rate = Column(Float, default=0)
    service_radius_km = Column(Float, default=10)
    verified = Column(Boolean, default=False)
    available = Column(Boolean, default=True)
    rating = Column(Float, default=0)
    completed_jobs = Column(Integer, default=0)
    city = Column(String(100), default="Bengaluru")

    user = relationship("User", back_populates="worker")
    service = relationship("ServiceCategory", back_populates="workers")
    kyc = relationship("WorkerKYC", back_populates="worker", uselist=False, cascade="all, delete-orphan")

class WorkerKYC(Base):
    __tablename__ = "worker_kyc"
    id = Column(Integer, primary_key=True)
    worker_id = Column(Integer, ForeignKey("workers.id"), unique=True, nullable=False)
    legal_name = Column(String(120), nullable=False)
    dob = Column(String(20), nullable=True)
    address = Column(Text, nullable=False)
    aadhaar_last4 = Column(String(4), nullable=True)
    pan_masked = Column(String(20), nullable=True)
    aadhaar_front = Column(String(255), nullable=True)
    aadhaar_back = Column(String(255), nullable=True)
    pan_document = Column(String(255), nullable=True)
    selfie = Column(String(255), nullable=True)
    status = Column(String(30), default="PENDING")
    rejection_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    worker = relationship("Worker", back_populates="kyc")

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    worker_id = Column(Integer, ForeignKey("workers.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("service_categories.id"), nullable=False)
    address = Column(Text, nullable=False)
    scheduled_at = Column(DateTime, nullable=False)
    description = Column(Text, default="")
    budget = Column(Float, default=0)
    status = Column(String(30), default="PENDING", index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("User", foreign_keys=[customer_id], back_populates="bookings_as_customer")
    worker_user = relationship("User", foreign_keys=[worker_id], primaryjoin="Booking.worker_id==Worker.id", viewonly=True)
    worker = relationship("Worker", foreign_keys=[worker_id])
    service = relationship("ServiceCategory")
    review = relationship("Review", back_populates="booking", uselist=False, cascade="all, delete-orphan")

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    worker_id = Column(Integer, ForeignKey("workers.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    booking = relationship("Booking", back_populates="review")

class Favorite(Base):
    __tablename__ = "favorites"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    worker_id = Column(Integer, ForeignKey("workers.id"), nullable=False)

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
