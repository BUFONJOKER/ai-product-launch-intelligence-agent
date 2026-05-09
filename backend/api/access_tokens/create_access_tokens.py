from datetime import datetime, timedelta
from jose import jwt
from config import ACCESS_TOKEN_SECRET_KEY

SECRET_KEY = ACCESS_TOKEN_SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(datetime.timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    access_token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return access_token