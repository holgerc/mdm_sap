"""Pydantic schemas for authentication."""
from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema."""
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a user."""
    password: str = Field(..., min_length=8)
    role_id: Optional[UUID] = None


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role_id: Optional[UUID] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """Schema for user response."""
    id: UUID
    role_id: Optional[UUID] = None
    is_superuser: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Schema for JWT token payload."""
    sub: str
    exp: int


class LoginRequest(BaseModel):
    """Schema for login request."""
    username: str
    password: str


class RoleBase(BaseModel):
    """Base role schema."""
    role_code: str = Field(..., min_length=1, max_length=50)
    role_name: str = Field(..., min_length=1, max_length=200)
    role_description: Optional[str] = None
    is_system: bool = False


class RoleCreate(RoleBase):
    """Schema for creating a role."""
    pass


class RoleResponse(RoleBase):
    """Schema for role response."""
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
