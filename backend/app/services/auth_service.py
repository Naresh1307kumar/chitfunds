from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User, UserRole, UserStatus, KYCStatus
from app.utils.password import hash_password, verify_password
from app.utils.jwt import create_access_token, create_refresh_token, verify_token
from app.schemas.auth import RegisterRequest, LoginRequest
from datetime import datetime

MAX_FAILED_ATTEMPTS = 5


def register_member(db: Session, data: RegisterRequest) -> User:
    # Check duplicate username
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    # Check duplicate aadhar
    if data.aadhar_number and db.query(User).filter(User.aadhar_number == data.aadhar_number).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Aadhar number already registered"
        )

    user = User(
        username=data.username,
        name=data.name,
        email=data.email,
        phone=data.phone,
        aadhar_number=data.aadhar_number if data.aadhar_number else None,
        password_hash=hash_password(data.password),
        role=UserRole.member,
        status=UserStatus.pending,
        kyc_status=KYCStatus.not_submitted,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, data: LoginRequest, required_role: UserRole) -> dict:
    from sqlalchemy import or_
    user = db.query(User).filter(
        or_(User.username == data.username, User.email == data.username),
        User.is_deleted == False
    ).first()

    # User not found
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    # Role mismatch
    if user.role != required_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied for this login portal"
        )

    # Account locked
    if user.failed_login_attempts >= MAX_FAILED_ATTEMPTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Account locked due to too many failed attempts. Contact admin."
        )

    # Wrong password
    if not verify_password(data.password, user.password_hash):
        user.failed_login_attempts += 1
        db.commit()
        remaining = MAX_FAILED_ATTEMPTS - user.failed_login_attempts
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid email or password. {remaining} attempts remaining."
        )


    # Member rejected or suspended
    if user.status in [UserStatus.rejected, UserStatus.suspended]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Your account is {user.status.value}. Contact admin."
        )

    # Success — reset failed attempts, update last login
    user.failed_login_attempts = 0
    user.last_login = datetime.utcnow()
    db.commit()
    db.refresh(user)

    token_data = {"sub": str(user.id), "role": user.role.value}
    return {
        "access_token": create_access_token(token_data),
        "refresh_token": create_refresh_token(token_data),
        "token_type": "bearer",
        "user": user
    }


def refresh_access_token(refresh_token: str) -> dict:
    payload = verify_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    token_data = {"sub": payload["sub"], "role": payload["role"]}
    return {
        "access_token": create_access_token(token_data),
        "token_type": "bearer"
    }


def change_password(db: Session, user: User, current_password: str, new_password: str):
    if not verify_password(current_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    user.password_hash = hash_password(new_password)
    db.commit()
    return {"message": "Password changed successfully"}


def get_me(user: User) -> User:
    return user


import random
from datetime import timedelta
from app.models.password_reset import PasswordReset
from app.services.notification_service import send_email_mock

def forgot_password(db: Session, username: str):
    from sqlalchemy import func
    user = db.query(User).filter(
        (func.lower(User.username) == func.lower(username.strip())) |
        (func.lower(User.email) == func.lower(username.strip())),
        User.is_deleted == False
    ).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No registered account found with this username or email."
        )

    # Invalidate previous unused OTPs for this user
    db.query(PasswordReset).filter(
        PasswordReset.user_id == user.id,
        PasswordReset.is_used == False
    ).update({"is_used": True})

    # Generate 6-digit numeric OTP
    otp = f"{random.randint(100000, 999999)}"
    expires = datetime.utcnow() + timedelta(minutes=15)

    reset_entry = PasswordReset(
        user_id=user.id,
        reset_token=otp,
        expires_at=expires,
        is_used=False
    )
    db.add(reset_entry)
    db.commit()

    # Dispatch email with OTP to registered email
    subject = "SecureChit - Password Reset OTP Code"
    body = f"""Hello {user.name},

You requested to reset your password for your SecureChit account ({user.username}).

Your 6-Digit Password Reset OTP is:
========================================
{otp}
========================================

This OTP is valid for 15 minutes. Please enter this OTP in the application to reset your password.
If you did not request this, please ignore this email.

Best Regards,
SecureChit Security Team
"""
    try:
        send_email_mock(user.email, subject, body)
    except Exception as e:
        print("Failed to dispatch email:", e)

    # Mask email for display (e.g. n***3@gmail.com)
    parts = user.email.split("@")
    if len(parts) == 2:
        local, domain = parts
        if len(local) <= 2:
            masked_email = f"{local[0]}*@{domain}"
        else:
            masked_email = f"{local[0]}{'*' * (len(local) - 2)}{local[-1]}@{domain}"
    else:
        masked_email = user.email

    return {
        "message": f"OTP has been sent successfully to your registered email ({masked_email}).",
        "email": masked_email,
        "username": user.username,
        "reset_token_debug": otp
    }


def reset_password(db: Session, token: str, new_password: str, username: str = None):
    from sqlalchemy import func
    target_otp = (token or "").strip()

    query = db.query(PasswordReset).filter(
        PasswordReset.reset_token == target_otp,
        PasswordReset.is_used == False,
        PasswordReset.expires_at > datetime.utcnow()
    )

    if username:
        user_match = db.query(User).filter(
            (func.lower(User.username) == func.lower(username.strip())) |
            (func.lower(User.email) == func.lower(username.strip()))
        ).first()
        if user_match:
            query = query.filter(PasswordReset.user_id == user_match.id)

    reset_entry = query.order_by(PasswordReset.id.desc()).first()

    if not reset_entry:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP. Please enter the correct 6-digit code or request a new one."
        )

    user = db.query(User).filter(User.id == reset_entry.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password_hash = hash_password(new_password)
    reset_entry.is_used = True
    db.commit()

    return {"message": "Password reset successfully. You can now login with your new password."}
