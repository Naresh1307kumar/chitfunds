# Chit Fund Backend - Cloud Doc

### 1. Configuration Settings
Contains the environment variables and database URLs required for the application.

**backend/app/core/config.py**
```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Chit Fund Application"
    SECRET_KEY: str = "your-super-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "mysql+pymysql://user:password@localhost/chitfund_db"
    ENCRYPTION_KEY: str = "base64-encoded-fernet-key-here"

settings = Settings()
```

### 2. Database Connection
Creates the SQLAlchemy engine, session factory, and the base class for the models.

**backend/app/db/database.py**
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 3. Password Hashing and JWT Tokens
Contains the functions to hash and verify passwords with bcrypt and to create JWT tokens.

**backend/app/core/security.py**
```python
from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import jwt
import bcrypt
from app.core.config import settings

def hash_password(password: str) -> str:
    """Hash a plain password using bcrypt."""
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash."""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a new JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
```

### 4. Credential Encryption
Encrypts and decrypts sensitive data using Fernet.

**backend/app/utils/encryption.py**
```python
from cryptography.fernet import Fernet
from app.core.config import settings

# Initialize Fernet with the encryption key from settings
fernet = Fernet(settings.ENCRYPTION_KEY.encode())

def encrypt_data(data: str) -> str:
    """Encrypt a plain text string using Fernet."""
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str) -> str:
    """Decrypt a Fernet-encrypted string to plain text."""
    try:
        return fernet.decrypt(encrypted_data.encode()).decode()
    except Exception:
        return ""
```

### 5. Database Models
Defines the SQLAlchemy ORM models for Users and Chit Groups.

**backend/app/models/domain.py**
```python
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(50), index=True)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(100))
    chits = relationship("ChitGroup", back_populates="owner")

class ChitGroup(Base):
    __tablename__ = "chit_groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    total_value = Column(Float)
    months = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="chits")
```

### 6. User Schemas
Pydantic models for user data validation and serialization.

**backend/app/schemas/user.py**
```python
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    class Config:
        orm_mode = True
```

### 7. Chit Group Schemas
Pydantic models for Chit Group validation.

**backend/app/schemas/chit.py**
```python
from pydantic import BaseModel

class ChitBase(BaseModel):
    name: str
    total_value: float
    months: int

class ChitCreate(ChitBase):
    pass

class ChitResponse(ChitBase):
    id: int
    owner_id: int
    class Config:
        orm_mode = True
```

### 8. User CRUD Operations
Database operations for creating and retrieving users.

**backend/app/crud/crud_user.py**
```python
from sqlalchemy.orm import Session
from app.models.domain import User
from app.schemas.user import UserCreate
from app.core.security import hash_password

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

### 9. Chit Group CRUD Operations
Database operations for creating and retrieving chit groups.

**backend/app/crud/crud_chit.py**
```python
from sqlalchemy.orm import Session
from app.models.domain import ChitGroup
from app.schemas.chit import ChitCreate

def get_chits(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ChitGroup).offset(skip).limit(limit).all()

def create_chit(db: Session, chit: ChitCreate, owner_id: int):
    db_chit = ChitGroup(**chit.dict(), owner_id=owner_id)
    db.add(db_chit)
    db.commit()
    db.refresh(db_chit)
    return db_chit
```

### 10. API Dependencies
Provides database session injection and current user verification.

**backend/app/api/deps.py**
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.db.database import get_db
from app.core.config import settings
from app.crud.crud_user import get_user_by_email
from app.models.domain import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    user = get_user_by_email(db, email=email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### 11. Authentication Endpoints
API routes for user login and generating access tokens.

**backend/app/api/endpoints/auth.py**
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db.database import get_db
from app.crud.crud_user import get_user_by_email
from app.core.security import verify_password, create_access_token

router = APIRouter()

@router.post("/login")
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
```

### 12. User Management Endpoints
API routes for user registration and fetching profile details.

**backend/app/api/endpoints/users.py**
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.crud import crud_user
from app.db.database import get_db
from app.api.deps import get_current_user
from app.models.domain import User

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db=db, user=user)

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```

### 13. Chit Group Endpoints
API routes for managing and listing chit groups.

**backend/app/api/endpoints/chits.py**
```python
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.chit import ChitCreate, ChitResponse
from app.crud import crud_chit
from app.db.database import get_db
from app.api.deps import get_current_user
from app.models.domain import User

router = APIRouter()

@router.post("/", response_model=ChitResponse)
def create_chit_group(chit: ChitCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_chit.create_chit(db=db, chit=chit, owner_id=current_user.id)

@router.get("/", response_model=List[ChitResponse])
def read_chits(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_chit.get_chits(db, skip=skip, limit=limit)
```

### 14. Main API Router
Combines all individual endpoint routers into a single API router.

**backend/app/api/api.py**
```python
from fastapi import APIRouter
from app.api.endpoints import auth, users, chits

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(chits.router, prefix="/chits", tags=["Chit Groups"])
```

### 15. Application Entry Point
Initializes the FastAPI application and includes the main router.

**backend/main.py**
```python
from fastapi import FastAPI
from app.api.api import api_router
from app.db.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Chit Fund API", version="1.0.0")

# Include the main API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Welcome to Chit Fund Management API"}
```
