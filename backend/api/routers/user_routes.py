from typing import List
from api.services import user_services
from api.schemas.user_data import (
    UserCreate,
    UserResponse,
    AddUserResponse,
    GetUser,
    GetUserResponse,
    UserAgentThreadResponse,
    UserCreateAgentThread,
)
from api.database.db_connection import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse
from api.access_tokens.create_access_tokens import create_access_token
import uuid

user_router = APIRouter(prefix="/api/users", tags=["users"])

# @user_router.get("/", response_model=List[UserResponse])
# def get_users(session: Session = Depends(get_db)):
#     return user_services.get_users(session)


@user_router.post("/login", response_model=GetUserResponse)
def get_user(get_user: GetUser, session: Session = Depends(get_db)):
    user = user_services.get_user(session, get_user.email, get_user.password)
    if user:
        return user
    raise HTTPException(status_code=401, detail="Invalid email or password")
    # try:
    #     user = user_services.get_user(session, get_user.email, get_user.password)
    #     if user is None:
    #         raise HTTPException(status_code=401, detail="Invalid email or password")
    #     else:
    #         access_token = create_access_token(data={"sub": user.email})

    #         return {
    #             "access_token": access_token,
    #             "token_type": "bearer",
    #             "message": "user logged in successfully",
    #         }
    # except HTTPException:
    #     raise
    # except Exception as exc:
    #     session.rollback()
    #     raise HTTPException(status_code=500, detail="Unable to login user") from exc


@user_router.post("/add_user", response_model=AddUserResponse, status_code=201)
def add_user(user: UserCreate, session: Session = Depends(get_db)):
    try:
        return user_services.add_user(session, user)
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(
            status_code=409, detail="A user with this email already exists"
        ) from exc
    except Exception as exc:
        session.rollback()
        raise HTTPException(status_code=500, detail="Unable to create user") from exc


@user_router.post(
    "/add_user_agent_thread_id", response_model=UserAgentThreadResponse, status_code=201
)
def add_user_agent_thread_id(
    user_agent_output: UserCreateAgentThread, session: Session = Depends(get_db)
):
    thread_id = str(uuid.uuid4())
    user = user_services.add_user_agent_thread(
            session, user_agent_output.email, thread_id
        )
    if user:
        return user
    raise HTTPException(status_code=401, detail="Invalid email or password")
    # try:
    #     thread_id = str(uuid.uuid4())
    #     return user_services.add_user_agent_thread(
    #         session, user_agent_output.email, user_agent_output.password, thread_id
    #     )
    # except IntegrityError as exc:
    #     session.rollback()
    #     raise HTTPException(
    #         status_code=409, detail="A user with this thread_id already exist"
    #     ) from exc
    # except Exception as exc:
    #     session.rollback()
    #     raise HTTPException(
    #         status_code=500, detail="Unable to create user thread_id"
    #     ) from exc


@user_router.put("/update_user", response_model=AddUserResponse)
def update_user(user: UserCreate, session: Session = Depends(get_db)):
    try:
        updated_user = user_services.update_user(session, user)
        if updated_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return updated_user
    except HTTPException:
        raise
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(
            status_code=409, detail="A user with this email already exists"
        ) from exc
    except Exception as exc:
        session.rollback()
        raise HTTPException(status_code=500, detail="Unable to update user") from exc


@user_router.delete("/delete_user")
def delete_user(user: UserCreate, session: Session = Depends(get_db)):
    try:
        deleted_user = user_services.delete_user(session, user)
        if deleted_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return JSONResponse(
            status_code=200, content={"message": "User deleted successfully"}
        )
    except HTTPException:
        raise
    except Exception as exc:
        session.rollback()
        raise HTTPException(status_code=500, detail="Unable to delete user") from exc
