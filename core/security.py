from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError  
from core.settings import settings
from core.exception import InvalidCredentials, Forbidden
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from dependencies.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def _normalize_password(password: str) -> str:
    if password is None:
        return ""
    return password.encode("utf-8")[:72].decode("utf-8", errors="ignore")


def hash_password(password: str):
    normalized_password = _normalize_password(password)
    return pwd_context.hash(normalized_password)


def verify_password(plain_password: str, hashed_password:str):
    normalized_plain_password = _normalize_password(plain_password)
    return pwd_context.verify(normalized_plain_password, hashed_password)

def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    return encoded_jwt

def create_access_token(user):
    return create_token(
        {
            "sub": str(user.id),
            "role": user.role,
            "type": "access"
        },
        timedelta(minutes=settings.access_token_expire_minutes)
    )

def create_refresh_token(user):
    return create_token(
        {
            "sub": str(user.id),
            "type": "refresh"
        },
        timedelta(days=settings.refresh_token_expire_days)
    )

def decode_token(token: str):
    try:
        payload  = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        sub = payload.get("sub")
        if sub is None:
            raise InvalidCredentials()
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token has expired"
        )
    except JWTError:
        raise InvalidCredentials()
    
    return payload

def decode_access_token(token: str):
    payload = decode_token(token)

    if payload.get("type") != "access":
        raise InvalidCredentials()

    return payload

def decode_refresh_token(token: str):
    payload = decode_token(token)

    if payload.get("type") != "refresh":
        raise InvalidCredentials()

    return payload

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    from services.user_service import UserSerise

    payload = decode_access_token(token)

    user_id = int(payload["sub"])

    service = UserSerise(db=db)

    user = service.get_user_by_id(user_id)

    if user is None:
        raise InvalidCredentials()

    return user


def requires_role(*roles):
    def checker(current_user = Depends(get_current_user)):
        if current_user.role not in roles:
            raise Forbidden(current_user.role)
        return current_user
    return checker
