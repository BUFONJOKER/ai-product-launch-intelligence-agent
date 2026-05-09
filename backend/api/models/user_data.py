from api.database.db_connection import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped


class UserData(Base):
    __tablename__ = "user_data"

    """ORM model representing a registered user.

    Columns:
        id (int): Primary key, auto-incrementing user id.
        name (str): User's display name.
        email (str): User email address (unique).
        password (str): Hashed password string.
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
