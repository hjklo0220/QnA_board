import datetime

from fastapi import Depends
from passlib.context import CryptContext
from jose import jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = "ee73e3d5c347845c08e32acf32e5da62dca77c8910a1e036faad6145a5152291"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    # encoding: str = "UTF-8"
    # secret_key: str = "60440b2e680235a5823ff9382bd9e50b15f9b28cc9324c6be8b27cf6e19dc482"
    # jwt_algorithm: str = "HS256"

    def hash_password(self, plain_password: str) -> str:
        return pwd_context.hash(plain_password)
    
    def verify_password(self, input_password: str, user_password: str) -> bool:
        return pwd_context.verify(input_password, user_password)
    
    def create_access_token(self, username: str) -> str:
        return jwt.encode(
            {
                "sub": username,
                "exp": datetime.datetime.now() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            },
            SECRET_KEY,
            algorithm=ALGORITHM,
        )

