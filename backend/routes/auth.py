"""
Authentication endpoints for Phase II Todo App
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from backend.models import User, UserCreate, UserRead
from backend.db import get_session
from backend.auth import get_password_hash, create_access_token, authenticate_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserCreate,
    session: Session = Depends(get_session),
):
    """
    Register a new user.
    
    Args:
        user_data: User registration data (email, name, password)
        session: Database session
        
    Returns:
        Created user data (without password)
    """
    # Check if user already exists
    result = session.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalars().first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    # Hash the password
    hashed_password = get_password_hash(user_data.password)
    
    # Create new user
    db_user = User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=hashed_password
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    # Return user data without password
    return db_user


@router.post("/login")
def login_user(
    email: str,
    password: str,
    session: Session = Depends(get_session),
):
    """
    Login a user and return JWT token.
    
    Args:
        email: User's email address
        password: User's password
        session: Database session
        
    Returns:
        JWT access token
    """
    user = authenticate_user(email, password, session)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create and return access token
    access_token = create_access_token(user_id=user.id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }