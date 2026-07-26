from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def _normalize_password(password: str) -> str:
    if password is None:
        return ""
    return password.encode("utf-8")[:72].decode("utf-8", errors="ignore")

def verify_password(plain_password: str, hashed_password:str):
    normalized_plain_password = _normalize_password(plain_password)
    return pwd_context.verify(normalized_plain_password, hashed_password)

print(verify_password("123123", "$2b$12$TtO8vgI7mlwtSs6tWYjuq.tC.Dp2xn5nKJnMKYaBM4ZnQzcqFQMqK"))



