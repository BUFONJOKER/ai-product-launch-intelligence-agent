from fastapi import APIRouter
from pydantic import BaseModel, Field, EmailStr
from api.password_hash.hash_password import get_password_hash

class SignupRequest(BaseModel):
    name: str = Field(..., example="User name")
    email: EmailStr = Field(..., example="email@email.com")
    password: str = Field(..., example="password123")

router = APIRouter()



@router.post("/signup")
async def signup(signup_request: SignupRequest):

    name = signup_request.name
    email = signup_request.email
    password = signup_request.password

    # hash passowrd
    hashed_password = get_password_hash(password)
    
    # save all to database
