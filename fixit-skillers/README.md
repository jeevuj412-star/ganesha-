# Fixit Skillers

Full-stack skilled-services marketplace MVP.

## Stack
- Frontend: React + Vite + Tailwind CSS
- Backend: FastAPI + SQLAlchemy + PostgreSQL
- Auth: JWT + bcrypt
- Docker Compose

## Features
- Customer / Worker / Admin roles
- Registration and login
- Service categories
- Worker profiles
- Worker KYC submission
- Customer booking
- Worker accept/reject/start/complete booking
- Admin KYC approval/rejection
- Ratings/reviews
- Responsive dashboard UI

## Run with Docker

1. Copy `.env.example` to `.env`
2. Run:
   `docker compose up --build`
3. Frontend: http://localhost:5173
4. API docs: http://localhost:8000/docs

## Demo admin
Email: admin@fixitskillers.local
Password: Admin@123

For production, change this password and JWT secrets.

## Local backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Local frontend
```bash
cd frontend
npm install
npm run dev
```

Set `VITE_API_URL=http://localhost:8000/api` in frontend/.env if needed.

This is an MVP foundation. Before production, add real SMS/OTP, secure KYC storage, payment gateway, object storage, rate limiting, audit logging, background jobs, and legal/privacy compliance.
