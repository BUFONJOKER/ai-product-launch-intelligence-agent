from api.services import user_services
from api.schemas.user_data import (
    LoginRequest,
    LoginResponse,
    SignUpRequest,
    SignUpResponse,
    CreateThreadRequest,
    CreateThreadResponse,
)
from api.database.db_connection import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse
from api.access_tokens.create_access_tokens import create_access_token
import uuid

user_router = APIRouter(prefix="/api/users", tags=["users"])


@user_router.post("/login", response_model=LoginResponse)
def get_user(request: LoginRequest, session: Session = Depends(get_db)):
    """Authenticate a user and return an access token with user details.

    This endpoint validates the user's email and password credentials against the
    database. On successful authentication, it generates a JWT access token and
    returns the user's profile information including name, email, and encrypted
    OpenAI API key for subsequent agent requests.

    Args:
        request (LoginRequest): The login request containing email and password.
        session (Session): SQLAlchemy database session provided by dependency injection.

    Returns:
        LoginResponse: A response object containing:
            - access_token (str): JWT bearer token for authenticated requests
            - token_type (str): Token type (always 'bearer')
            - name (str): User's full name
            - email (str): User's email address
            - api_key_openai (str): User's encrypted OpenAI API key
            - message (str): Success confirmation message

    Raises:
        HTTPException: 401 status code if email or password is invalid.
    """
    try:
        user = user_services.get_user(session, request.email, request.password)
        if user:
            access_token = create_access_token(data={"sub": user["email"]})
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "name": user["name"],
                "email": user["email"],
                "api_key_openai": user["api_key_openai"],
                "message": "User retrieved successfully",
            }
        raise HTTPException(status_code=401, detail="Invalid email or password")
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail="An error occurred during login authentication"
        ) from exc


@user_router.get("/get_user_threads/{email}")
def get_user_threads(email: str, session: Session = Depends(get_db)):
    """Retrieve all threads associated with a specific user.

    Args:
        email (str): The email address of the user whose threads are to be retrieved.
        session (Session): SQLAlchemy database session provided by dependency injection.

    Returns:
        List[Thread]: A list of threads associated with the specified user.

    Raises:
        HTTPException: 404 status code if no threads are found for the specified user.
    """

    try:
        threads = user_services.get_user_threads(session, email)
        if threads is not None:
            return threads
        raise HTTPException(
            status_code=404, detail="No threads found for the specified user."
        )
    except HTTPException:
        raise

@user_router.post("/signup", response_model=SignUpResponse, status_code=201)
def add_user(request: SignUpRequest, session: Session = Depends(get_db)):
    """Create a new user account with credentials and OpenAI API key.

    This endpoint registers a new user by storing their name, email, hashed password,
    and encrypted OpenAI API key in the database. It performs validation to ensure
    the email is unique and handles integrity errors gracefully.

    Args:
        request (SignUpRequest): The signup request containing name, email, password,
            and encrypted api_key_openai.
        session (Session): SQLAlchemy database session provided by dependency injection.

    Returns:
        SignUpResponse: A response object containing:
            - name (str): User's full name
            - email (str): User's registered email address
            - api_key_openai (str): User's encrypted OpenAI API key
            - message (str): Success confirmation message

    Raises:
        HTTPException: 409 status code if a user with the provided email already exists.
        HTTPException: 500 status code if an unexpected error occurs during user creation.
    """
    try:
        return user_services.add_user(session, request)
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email already registered. Please use a different email address.",
        ) from exc
    except HTTPException:
        raise
    except Exception as exc:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to create user account. Please try again later.",
        ) from exc


@user_router.post(
    "/add_user_agent_thread_id", response_model=CreateThreadResponse, status_code=201
)
def add_user_agent_thread_id(
    request: CreateThreadRequest, session: Session = Depends(get_db)
):
    """Create and associate a new workflow thread ID with a user account.

    This endpoint generates a unique UUID for a new agent workflow thread and links
    it to the user's account by email. This thread ID is subsequently used to
    maintain thread-specific state and conversation history across multiple agent runs.

    Args:
        request (CreateThreadRequest): The request containing the user's email address.
        session (Session): SQLAlchemy database session provided by dependency injection.

    Returns:
        CreateThreadResponse: A response object containing:
            - thread_id (str): The newly generated UUID for the workflow thread
            - email (str): The user's email address
            - message (str): Success confirmation message

    Raises:
        HTTPException: 401 status code if the email does not correspond to an existing user.
    """
    try:
        thread_id = str(uuid.uuid4())
        user = user_services.add_user_agent_thread(session, request.email, thread_id)
        if user:
            return user
        raise HTTPException(
            status_code=401, detail="User not found. Please check the email address."
        )
    except HTTPException:
        raise
    except Exception as exc:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to create workflow thread. Please try again later.",
        ) from exc


@user_router.put("/update_user", response_model=SignUpResponse)
def update_user(user: SignUpRequest, session: Session = Depends(get_db)):
    """Update an existing user's profile information and credentials.

    This endpoint allows users to update their name, email, password, and/or OpenAI
    API key. It enforces email uniqueness during updates and handles errors gracefully.

    Args:
        user (SignUpRequest): The user object containing updated values for name, email,
            password, and/or api_key_openai.
        session (Session): SQLAlchemy database session provided by dependency injection.

    Returns:
        SignUpResponse: A response object containing:
            - name (str): Updated user's full name
            - email (str): Updated user's email address
            - api_key_openai (str): Updated encrypted OpenAI API key
            - message (str): Success confirmation message

    Raises:
        HTTPException: 404 status code if the user is not found in the database.
        HTTPException: 409 status code if the new email is already associated with another user.
        HTTPException: 500 status code if an unexpected error occurs during the update.
    """
    try:
        updated_user = user_services.update_user(session, user)
        if updated_user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found. Cannot update non-existent account.",
            )
        return updated_user
    except HTTPException:
        raise
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email already in use by another account. Please choose a different email.",
        ) from exc
    except Exception as exc:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to update user profile. Please try again later.",
        ) from exc


@user_router.delete("/delete_user")
def delete_user(user: SignUpRequest, session: Session = Depends(get_db)):
    """Permanently delete a user account and all associated data.

    This endpoint removes a user from the database by matching email and password.
    Upon successful deletion, all associated user data, threads, and API keys are
    permanently removed.

    Args:
        user (SignUpRequest): The user object containing email and password for
            identity verification before deletion.
        session (Session): SQLAlchemy database session provided by dependency injection.

    Returns:
        JSONResponse: A JSON response with status code 200 and a success message:
            {"message": "User deleted successfully"}

    Raises:
        HTTPException: 404 status code if the user is not found in the database.
        HTTPException: 500 status code if an unexpected error occurs during deletion.
    """
    try:
        deleted_user = user_services.delete_user(session, user)
        if deleted_user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found. Cannot delete non-existent account.",
            )
        return JSONResponse(
            status_code=200,
            content={
                "message": "User account deleted successfully. All associated data has been removed."
            },
        )
    except HTTPException:
        raise
    except Exception as exc:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to delete user account. Please try again later.",
        ) from exc
