%%writefile /content/backend/api/routes/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field

from database.crud import create_user, get_user_by_email
from backend.api.dependencies import get_database
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

    hashed_password = hash_password(
        user_data.password
    )

    user = create_user(
        db,
        user_data.username,
        user_data.email,
        hashed_password
    )

    return {
        "message": "User registered successfully",
        "user_id": user.id,
        "username": user.username,
        "email": user.email
    }
