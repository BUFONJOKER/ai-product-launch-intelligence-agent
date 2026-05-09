from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UserCreate(BaseModel):
    """Schema for creating a new user (input payload).

    Used in POST/PUT requests to create or update users. Includes the
    plain-text password which should be hashed before storage.

    Attributes:
        name (str): User display name.
        email (EmailStr): User email address.
        password (str): Plain-text password (will be hashed before storage).
    """

    name: str = Field(..., description="The user's display name")
    email: EmailStr = Field(..., description="The user's email address")
    password: str = Field(..., description="The user's password")


class UserResponse(BaseModel):
    """Schema for user API responses (output payload).

    Returned by GET/POST/PUT endpoints. Excludes the password field for
    security—never expose password hashes in API responses.

    Attributes:
        id (int): Unique user identifier.
        name (str): User display name.
        email (EmailStr): User email address.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="The unique identifier of the user")
    name: str = Field(..., description="The user's display name")
    email: EmailStr = Field(..., description="The user's email address")


