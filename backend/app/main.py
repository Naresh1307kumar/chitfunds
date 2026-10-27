from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from app.config import APP_NAME, APP_VERSION, FRONTEND_URL, DEBUG
import os

# Import all models so SQLAlchemy creates tables
from app.models import (
    User, KYCDocument, Guarantor, ChitPlan, PlanMember,
    Installment, Payment, MonthlyDraw, Notification, Certificate, Report, AuditLog,
    PasswordReset, SystemSetting, PromissoryNote
)

# Import routers
from app.routers import auth
from app.routers.admin import members as admin_members
from app.routers.admin import kyc as admin_kyc
from app.routers.admin import plans as admin_plans
from app.routers.admin import draws as admin_draws
from app.routers.admin import dashboard as admin_dashboard
from app.routers.admin import payments as admin_payments
from app.routers.admin import reports as admin_reports
from app.routers.admin import pronotes as admin_pronotes
from app.routers.member import profile as member_profile
from app.routers.member import kyc as member_kyc
from app.routers.member import plans as member_plans
from app.routers.member import payments as member_payments
from app.routers.member import notifications as member_notifications
from app.routers.member import pronotes as member_pronotes
from app.routers import public

# Create all tables safely
try:
    Base.metadata.create_all(bind=engine)
    print("Database tables verified/created successfully.")
except Exception as e:
    print(f"Warning: Database connection / table creation error on startup: {e}")

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Secure Chit Fund Management System API",
    docs_url="/docs" if DEBUG else None,
    redoc_url="/redoc" if DEBUG else None,
)

# CORS
origins = [
    "https://chitfunds-two.vercel.app",
    FRONTEND_URL,
    "http://localhost:5173", "http://localhost:5174", "http://localhost:5175",
    "http://localhost:5176", "http://localhost:5177", "http://localhost:5178",
    "http://localhost:5179", "http://localhost:5180", "http://localhost:5181",
    "http://127.0.0.1:5173", "http://127.0.0.1:5174", "http://127.0.0.1:5178",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for uploads
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Register routers
app.include_router(public.router)
app.include_router(auth.router)
app.include_router(admin_members.router, prefix="/api/v1/admin")
app.include_router(admin_kyc.router, prefix="/api/v1/admin/kyc")
app.include_router(admin_plans.router, prefix="/api/v1/admin/plans")
app.include_router(admin_draws.router)
app.include_router(admin_dashboard.router)
app.include_router(admin_payments.router, prefix="/api/v1/admin")
app.include_router(admin_reports.router, prefix="/api/v1/admin")
app.include_router(admin_pronotes.router, prefix="/api/v1/admin")
app.include_router(member_profile.router, prefix="/api/v1/member")
app.include_router(member_kyc.router, prefix="/api/v1/member/kyc")
app.include_router(member_plans.router, prefix="/api/v1/member/plans")
app.include_router(member_payments.router, prefix="/api/v1/member")
app.include_router(member_notifications.router, prefix="/api/v1/member")
app.include_router(member_pronotes.router, prefix="/api/v1/member")


@app.get("/")
def root():
    return {"message": f"{APP_NAME} API is running", "version": APP_VERSION}


@app.get("/health")
def health_check():
    return {"status": "healthy", "app": APP_NAME}
