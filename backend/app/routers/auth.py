from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import (
    RegisterRequest, LoginRequest, TokenResponse,
    UserResponse, RefreshTokenRequest, ChangePasswordRequest,
    ForgotPasswordRequest, ResetPasswordRequest
)
from app.services import auth_service
from app.middleware.auth import get_current_user
from app.models.user import User, UserRole

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


# ─── Member Register ─────────────────────────────────────
@router.post("/register", response_model=UserResponse, status_code=201)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    """Public — Member self registration"""
    user = auth_service.register_member(db, data)
    return user


# ─── Member Login ────────────────────────────────────────
@router.post("/member/login", response_model=TokenResponse)
def member_login(data: LoginRequest, db: Session = Depends(get_db)):
    """Member login portal"""
    result = auth_service.login_user(db, data, required_role=UserRole.member)
    return result


# ─── Admin Login ─────────────────────────────────────────
@router.post("/admin/login", response_model=TokenResponse)
def admin_login(data: LoginRequest, db: Session = Depends(get_db)):
    """Admin login portal"""
    result = auth_service.login_user(db, data, required_role=UserRole.admin)
    return result


# ─── Get Current User ────────────────────────────────────
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Get logged-in user details"""
    return current_user


# ─── Refresh Token ───────────────────────────────────────
@router.post("/refresh-token")
def refresh_token(data: RefreshTokenRequest):
    """Generate new access token using refresh token"""
    return auth_service.refresh_access_token(data.refresh_token)


# ─── Change Password ─────────────────────────────────────
@router.put("/change-password")
def change_password(
    data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change password for logged-in user"""
    return auth_service.change_password(
        db, current_user, data.current_password, data.new_password
    )


# ─── Forgot / Reset Password ────────────────────────────
@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """Request password reset link"""
    return auth_service.forgot_password(db, data.username)

@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Reset password using token"""
    return auth_service.reset_password(db, data.token, data.new_password)


# ─── Logout ──────────────────────────────────────────────
@router.post("/logout")
def logout():
    """Logout — client should delete token"""
    return {"message": "Logged out successfully"}
