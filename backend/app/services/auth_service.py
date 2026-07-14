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
    user = db.query(User).filter(
        User.username == data.username,
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


import uuid
from datetime import timedelta
from app.models.password_reset import PasswordReset

def forgot_password(db: Session, username: str):
    user = db.query(User).filter(User.username == username, User.is_deleted == False).first()
    if not user:
        # Don't reveal if username exists or not for security
        return {"message": "If the username is registered, a password reset link will be sent."}
    
    # Generate token
    token = str(uuid.uuid4())
    expires = datetime.utcnow() + timedelta(hours=1)
    
    reset_entry = PasswordReset(
        user_id=user.id,
        reset_token=token,
        expires_at=expires
    )
    db.add(reset_entry)
    db.commit()
    
    # In a real app, send email here. For now, we return the token for testing.
    return {"message": "If the email is registered, a password reset link will be sent.", "reset_token_debug": token}


def reset_password(db: Session, token: str, new_password: str):
    reset_entry = db.query(PasswordReset).filter(
        PasswordReset.reset_token == token,
        PasswordReset.is_used == False,
        PasswordReset.expires_at > datetime.utcnow()
    ).first()
    
    if not reset_entry:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
        
    user = db.query(User).filter(User.id == reset_entry.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user.password_hash = hash_password(new_password)
    reset_entry.is_used = True
    db.commit()
    
    return {"message": "Password reset successfully. You can now login."}
