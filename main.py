
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from dependencies import get_db, get_current_user
from models.users import User
from schemas import UserRegister
from security import (
    create_access_token,
    hash_password,
    verify_password,
)

app = FastAPI(
    title="Authentication System API",
    description="A REST API for user registration and authentication.",
    version="1.0.0",
)


@app.post("/register", status_code=201)
def register(
    user: UserRegister,
    db: Session = Depends(get_db),
):
    statement = select(User).where(
        (User.username == user.username)
        | (User.email == user.email)
    )

    existing_user = db.execute(
        statement
    ).scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Username or email already exists",
        )

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Username or email already exists",
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database operation failed",
        )

    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "is_active": new_user.is_active,
    }


@app.post("/login")
def login(
    user: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    statement = select(User).where(
        User.username == user.username
    )

    existing_user = db.execute(
        statement
    ).scalar_one_or_none()

    if (
        existing_user is None
        or not verify_password(
            user.password,
            existing_user.hashed_password,
        )
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not existing_user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User account is inactive",
        )

    access_token = create_access_token(
        {"sub": str(existing_user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@app.get("/me")
def get_me(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
    }
