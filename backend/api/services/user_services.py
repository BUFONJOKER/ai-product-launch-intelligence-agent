from sqlalchemy.orm import Session

from api.models.user_data import UserData
from api.schemas.user_data import UserCreate, UserResponse
from api.password_hash.hash_password import get_password_hash
from api.password_hash.verify_password import verify_password

def create_user(db: Session, user_data: UserCreate):
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
    user.password= password_hash
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def update_user(db: Session, user_id: int, user_data: UserCreate):
    """Update an existing user's fields.

    Args:
        db (Session): SQLAlchemy session.
        user_id (int): ID of the user to update.
        user_data (UserCreate): Schema containing updated fields.

    Returns:
        UserData | None: The updated ORM instance if found, otherwise
            `None` when the user does not exist.
    """

    user = db.query(UserData).filter(UserData.id == user_id).first()

    if not user:
        return None

    for key, value in user_data.model_dump().items():
        if key == "password":
            value = get_password_hash(value)
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user


def delete_user(db: Session, user_id: int):
    """Delete a user by ID.

    Args:
        db (Session): SQLAlchemy session.
        user_id (int): ID of the user to delete.

    Returns:
        bool | None: `True` if deletion succeeded, `None` if user not found.
    """

    user = db.query(UserData).filter(UserData.id == user_id).first()

    if not user:
        return None

    db.delete(user)
    db.commit()

    return True


def get_user(db: Session, user_id: int):
    """Retrieve a user ORM instance by ID.

    Args:
        db (Session): SQLAlchemy session.
        user_id (int): ID of the user to retrieve.

    Returns:
        UserData | None: The `UserData` ORM instance if found, otherwise
            `None`.
    """

    user = db.query(UserData).filter(UserData.id == user_id).first()

    if not user:
        return None

    return user


def get_users(db: Session):
    """Retrieve all users from the database.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        list[UserData]: List of all user ORM instances.
    """

    return db.query(UserData).all()


def add_user(db: Session, user_data: UserCreate):
    """Create a new user in the database (alias for create_user).

    Args:
        db (Session): SQLAlchemy session used for the transaction.
        user_data (UserCreate): Pydantic schema with user input fields.

    Returns:
        UserData: The newly created ORM `UserData` instance.
    """

    return create_user(db, user_data)
