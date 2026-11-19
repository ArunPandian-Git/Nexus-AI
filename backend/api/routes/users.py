%%writefile /content/backend/api/routes/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from database.crud import create_user, get_user_by_email
from backend.api.dependencies import get_database

router = APIRouter(prefix="/users", tags=["Users"])


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


@router.post("/")
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_database)
):
    existing_user = get_user_by_email(db, user_data.email)

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    # Temporary hash placeholder.
    # Secure password hashing will be implemented in the
    # authentication phase.
    user = create_user(
        db,
        user_data.username,
        user_data.email,
        "TEMPORARY_HASH_REPLACE_WITH_SECURE_HASHING"
    )

    return {
        "message": "User registered successfully",
        "user_id": user.id,
        "username": user.username,
        "email": user.email
    }


@router.get("/")
def list_users(db: Session = Depends(get_database)):
    from sqlalchemy import select
    from database.models import User

    users = db.scalars(select(User)).all()

    return {
        "total_users": len(users),
        "users": [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
            for user in users
        ]
    }
