from sqlalchemy.orm import Session

from api.models.user_data import UserData, UserAgentThread
from api.schemas.user_data import SignUpRequest
from api.password_hash.hash_password import get_password_hash
from api.password_hash.verify_password import verify_password
from api.api_key_encryption.encrypt_decrypt import encrypt_key, decrypt_key

def create_user(db: Session, user_data: SignUpRequest):
    """Create a new user in the database.

    Args:
        db (Session): SQLAlchemy session used for the transaction.
        user_data (UserCreate): Pydantic schema with user input fields.

    Returns:
        UserData: The newly created ORM `UserData` instance.
    """

    user = UserData(**user_data.model_dump())
    password = user_data.password
    password_hash = get_password_hash(password)
    user.password = password_hash
    user.api_key_openai = encrypt_key(user_data.api_key_openai)
    db.add(user)
    db.commit()
    db.refresh(user)

    if user.id is None:
        raise Exception("Failed to create user")

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "message": "User created successfully",
    }


def update_user(db: Session, user_data: SignUpRequest):
    """Update an existing user's fields.

    Args:
        db (Session): SQLAlchemy session.
        user_id (int): ID of the user to update.
        user_data (UserCreate): Schema containing updated fields.

    Returns:
        UserData | None: The updated ORM instance if found, otherwise
            `None` when the user does not exist.
    """

    user = db.query(UserData).filter(UserData.email == user_data.email).first()

    if not user:
        return None

    for key, value in user_data.model_dump().items():
        if key == "password":
            value = get_password_hash(value)
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "message": "User Updated Successfully",
    }


def delete_user(db: Session, user_data: SignUpRequest):
    """Delete a user by ID.

    Args:
        db (Session): SQLAlchemy session.
        user_data (UserCreate): Schema containing user email for deletion.

    Returns:
        bool | None: `True` if deletion succeeded, `None` if user not found.
    """

    user = db.query(UserData).filter(UserData.name == user_data.name, UserData.email == user_data.email).first()

    if not user:
        return None

    db.delete(user)
    db.commit()

    return True


def get_user(db: Session, email: str, password: str):
    """Retrieve a user ORM instance by email and password.

    Args:
        db (Session): SQLAlchemy session.
        email (str): Email address of the user to retrieve.
        password (str): Plain-text password for verification.


    Returns:
        UserData | None: The `UserData` ORM instance if found, otherwise
            `None`.
    """

    user = db.query(UserData).filter(UserData.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return {
        "name": user.name,
        "email": user.email,
        "api_key_openai": user.api_key_openai,
        "message": "User retrieved successfully",
    }


def get_user_threads(db: Session, email: str):
    """Retrieve all threads associated with a specific user.

    Args:
        db (Session): SQLAlchemy session.
        email (str): The email address of the user whose threads are to be retrieved.

    Returns:
        List[Thread]: A list of threads associated with the specified user.

    Raises:
        HTTPException: 404 status code if no threads are found for the specified user.
    """
    threads = db.query(UserAgentThread).filter(UserAgentThread.email == email).all()

    if not threads:
        return 'No threads found for the specified user'

    return [
        {
            "email": thread.email,
            "thread_id": thread.thread_id,
        }
        for thread in threads
    ]


def add_user(db: Session, user_data: SignUpRequest):
    """Create a new user in the database (alias for create_user).

    Args:
        db (Session): SQLAlchemy session used for the transaction.
        user_data (UserCreate): Pydantic schema with user input fields.

    Returns:
        UserData: The newly created ORM `UserData` instance.
    """

    return create_user(db, user_data)


def add_user_agent_thread(db: Session, email: str, thread_id: str):
    """Add a new user agent thread record to the database.

    This function creates a new entry in the `UserAgentThread` table with
    the provided email and thread ID. It can be used to log threads  from
    user agents for later retrieval.

    Args:
        db (Session): SQLAlchemy session used for the transaction.
        email (str): The email address associated with the user agent thread.
        thread_id (str): The unique thread ID for tracking the agent run.
    """

    user = UserAgentThread(email=email, thread_id=thread_id)

    db.add(user)
    db.commit()
    db.refresh(user)


    if user.id is None:
        raise Exception("Failed to create user agent thread")


    return {
        "email": user.email,
        "thread_id": user.thread_id,
        "message": "User agent thread created successfully",
    }

def delete_user_thread(db: Session, email: str, thread_id: str):
    """Delete a user agent thread record from the database.

    This function removes an entry from the `UserAgentThread` table that
    matches the provided email and thread ID. It can be used to clean up
    threads that are no longer needed.

    Args:
        db (Session): SQLAlchemy session used for the transaction.
        email (str): The email address associated with the user agent thread.
        thread_id (str): The unique thread ID for tracking the agent run.

    Returns:
        bool | None: `True` if deletion succeeded, `None` if no matching record was found.
    """

    user_thread = db.query(UserAgentThread).filter(UserAgentThread.email == email, UserAgentThread.thread_id == thread_id).first()

    if not user_thread:
        return None

    db.delete(user_thread)
    db.commit()

    return True