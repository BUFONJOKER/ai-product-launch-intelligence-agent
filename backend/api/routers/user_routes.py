from typing import List
from api.services import user_services
from api.schemas.user_data import UserCreate, UserResponse
from api.database.db_connection import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

user_router = APIRouter(prefix="/api/users", tags=["users"])


# @user_router.get("/", response_model=List[UserResponse])
# def get_users(session: Session = Depends(get_db)):
#     return user_services.get_users(session)


@user_router.get("/get_user/{user_id}", response_model=UserResponse)
def get_user(user_id: int, session: Session = Depends(get_db)):
    user = user_services.get_user(session, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.post("/add_user", response_model=UserResponse, status_code=201)
def add_user(user: UserCreate, session: Session = Depends(get_db)):
    return user_services.add_user(session, user)


@user_router.put("/update_user/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, session: Session = Depends(get_db)):
    updated_user = user_services.update_user(session, user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@user_router.delete("/delete_user/{user_id}", status_code=204)
def delete_user(user_id: int, session: Session = Depends(get_db)):
    deleted_user = user_services.delete_user(session, user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
