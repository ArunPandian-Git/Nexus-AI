%%writefile /content/backend/api/routes/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field

from database.crud import create_user, get_user_by_email
from database.models import User
from backend.api.dependencies import (
    get_database,
    get_current_user
)
from backend.core.security import hash_password

router = APIRouter(prefix="/users", tags=["Users"])


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


@router.post("/")
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_database)
):
    existing_user = get_user_by_email(
        db,
        user_data.email
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    user = create_user(
        db,
        user_data.username,
        user_data.email,
        hash_password(user_data.password)
    )

    return {
        "message": "User registered successfully",
        "user_id": user.id,
        "username": user.username,
        "email": user.email
    }


@router.get("/me")
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return {
        "user_id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "message": "Authenticated user profile retrieved"
    }
