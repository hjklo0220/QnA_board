from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from schema.user.response import UserSchema, TokenSchema
from service.user import UserService
from schema.user.request import LogInRequest, SignUpRequest
from db.repository import UserRepository
from db.orm import User

router = APIRouter(prefix="/user")

@router.post("/create", status_code=201)
def user_sign_up_handler(
    request: SignUpRequest,
    user_service: UserService = Depends(),
    user_repo: UserRepository = Depends(),
):
    hashed_password = user_service.hash_password(plain_password=request.password1)

    user: User | None = user_repo.get_existing_user(username=request.username)
    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    user: User = User.create(
        username=request.username,
        hashed_password=hashed_password,
        email=request.email,
    )

    user: User = user_repo.save_user(user=user)

    return UserSchema.from_orm(user)


@router.post("/login", status_code=201, response_model=TokenSchema)
def user_login_handler(
    request: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(),
    user_repo: UserRepository = Depends(),
) -> TokenSchema:
    user: User | None = user_repo.get_user(username=request.username)

    # check password
    verified: bool = user_service.verify_password(input_password=request.password, user_password=user.password)
    if not user or not verified:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # create access token -> return
    return TokenSchema(
        access_token=user_service.create_access_token(username=user.username),
        token_type="bearer",
        username=user.username,
    )
