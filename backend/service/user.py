from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError

from db.orm import User


ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = "ee73e3d5c347845c08e32acf32e5da62dca77c8910a1e036faad6145a5152291"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

class UserService:

    def hash_password(self, plain_password: str) -> str:
        return pwd_context.hash(plain_password)
    
    def verify_password(self, input_password: str, user_password: str) -> bool:
        return pwd_context.verify(input_password, user_password)
    
    def create_access_token(self, username: str) -> str:
        return jwt.encode(
            {
                "sub": username,
                "exp": datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            },
            SECRET_KEY,
            algorithm=ALGORITHM,
        )
    
    def decode_jwt(self, access_token: str) -> str:
        payload: dict = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])

        # expire
        if datetime.now() > datetime.fromtimestamp(payload["exp"]):
            raise HTTPException(status_code=401, detail="Token expired")
        
        return payload["sub"]
    
