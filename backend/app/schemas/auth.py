from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Optional
from app.models.user import UserRole, UserStatus


# ─── Registration ─────────────────────────────────────────
class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str
    aadhar_number: Optional[str] = None
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if not v.isalnum():
            raise ValueError("Username must be alphanumeric")
        return v.lower()

    @field_validator("aadhar_number")
    @classmethod
    def validate_aadhar(cls, v):
        if v:
            if not v.isdigit() or len(v) != 12:
                raise ValueError("Aadhar must be exactly 12 digits")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        if not v.isdigit() or len(v) != 10:
            raise ValueError("Phone must be 10 digits")
        return v


# ─── Login ──────────────────────────────────────────────
class LoginRequest(BaseModel):
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        return v.lower()


# ─── Token Response ─────────────────────────────────────
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: "UserResponse"


# ─── User Response ──────────────────────────────────────
class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    email: str
    phone: str
    role: UserRole
    status: UserStatus
    profile_photo: Optional[str] = None

    class Config:
        from_attributes = True


# ─── Refresh Token ──────────────────────────────────────
class RefreshTokenRequest(BaseModel):
    refresh_token: str


# ─── Change Password ────────────────────────────────────
class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


# ─── Forgot / Reset Password ────────────────────────────
class ForgotPasswordRequest(BaseModel):
    username: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        return v.lower()


class ResetPasswordRequest(BaseModel):
    token: Optional[str] = None
    otp: Optional[str] = None
    username: Optional[str] = None
    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


TokenResponse.model_rebuild()
