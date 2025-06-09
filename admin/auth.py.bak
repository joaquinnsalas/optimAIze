"""Authentication system for admin portal."""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from models import AdminUser, admin_db

# Security configuration
SECRET_KEY = "optimaize-admin-secret-key-change-in-production"  # TODO: Move to env var
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480  # 8 hours

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(db: Session, email: str, password: str) -> Optional[AdminUser]:
    """Authenticate user credentials."""
    user = db.query(AdminUser).filter(AdminUser.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    return user

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(admin_db.get_session)
) -> AdminUser:
    """Get current authenticated user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(AdminUser).filter(AdminUser.email == email).first()
    if user is None:
        raise credentials_exception
    
    return user

def create_admin_user(db: Session, email: str, password: str) -> AdminUser:
    """Create initial admin user."""
    # Check if any admin users exist
    existing_user = db.query(AdminUser).filter(AdminUser.email == email).first()
    if existing_user:
        return existing_user
    
    hashed_password = get_password_hash(password)
    admin_user = AdminUser(
        email=email,
        hashed_password=hashed_password,
        is_active=True
    )
    
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    
    return admin_user

def init_admin_user():
    """Initialize default admin user if none exists."""
    db = next(admin_db.get_session())
    try:
        # Check if any users exist
        user_count = db.query(AdminUser).count()
        if user_count == 0:
            # Create default admin
            create_admin_user(db, "admin@optimaize.com", "admin123")
            print("✅ Created default admin user: admin@optimaize.com / admin123")
            print("⚠️  Please change the password after first login!")
    finally:
        db.close()