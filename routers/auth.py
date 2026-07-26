from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from schemas.user import UserResponse, UserCreate, UserLogin
from schemas.auth import RefreshTokenRequest
from models.user import User
from dependencies.database import get_db
from services.user_service import UserSerise
from core.security import create_access_token, get_current_user, create_refresh_token, decode_refresh_token
from fastapi.security import OAuth2PasswordRequestForm
from core.exception import InvalidCredentials

router = APIRouter(prefix="/auth", tags=['Auth'])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    service = UserSerise(db)

    user = service.register_user(user_create)

    return user

@router.post("/login", status_code=status.HTTP_200_OK)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    service = UserSerise(db)

    class LoginPayload:
        username = form_data.username
        password = form_data.password

    user = service.log_in_user(LoginPayload)

    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/refresh")
def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    payload = decode_refresh_token( request.refresh_token)
    user_id = payload["sub"]
    service = UserSerise(db)

    user = service.get_user_by_id(user_id)

    if user is None:
        raise InvalidCredentials()
    
    access_token = create_access_token(user)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
