from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True
        from_attributes = True

class TokenSchema(BaseModel):
    access_token: str
    token_type: str
    username: str
