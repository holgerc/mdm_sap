"""Authentication endpoints."""
from datetime import timedelta
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.config import settings
from app.core.security import verify_password, get_password_hash, create_access_token, decode_token
from app.models.security import MDMUser, MDMRole
from app.schemas.auth import (
    Token, UserCreate, UserResponse, UserUpdate,
    RoleCreate, RoleResponse, LoginRequest
)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> MDMUser:
    """Get current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception

    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    result = await db.execute(
        select(MDMUser).where(MDMUser.username == username, MDMUser.is_active == True)
    )
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """Authenticate user and return access token."""
    result = await db.execute(
        select(MDMUser).where(MDMUser.username == form_data.username)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token)


@router.post("/register", response_model=UserResponse)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user."""
    # Check if user exists
    result = await db.execute(
        select(MDMUser).where(
            (MDMUser.username == user_data.username) | (MDMUser.email == user_data.email)
        )
    )
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )

    # Create user
    user = MDMUser(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=get_password_hash(user_data.password),
        role_id=user_data.role_id
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: MDMUser = Depends(get_current_user)
):
    """Get current user information."""
    return current_user


@router.get("/users", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: MDMUser = Depends(get_current_user)
):
    """List all users (admin only)."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    result = await db.execute(
        select(MDMUser).where(MDMUser.is_active == True).offset(skip).limit(limit)
    )
    return result.scalars().all()


# Role endpoints
@router.post("/roles", response_model=RoleResponse)
async def create_role(
    role_data: RoleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: MDMUser = Depends(get_current_user)
):
    """Create a new role."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    role = MDMRole(**role_data.model_dump())
    db.add(role)
    await db.commit()
    await db.refresh(role)
    return role


@router.get("/roles", response_model=List[RoleResponse])
async def list_roles(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """List all roles."""
    result = await db.execute(
        select(MDMRole).where(MDMRole.is_active == True).offset(skip).limit(limit)
    )
    return result.scalars().all()
