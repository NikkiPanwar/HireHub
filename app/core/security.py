from datetime import datetime ,timedelta , timezone
import bcrypt 
from jose import jwt , JWTError
from app.core.config import settings


def hash_password(password:str)->str:
    """to convet plan password to hash password"""
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes,salt).decode("utf-8")



def verify_password(plain_password:str,hashed_password:str)-> bool:
    """ used to check the password during login time"""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """used to generate jwt and add role and user id here"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(
            refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id = payload.get("sub")

        if not user_id:
            return None

        return payload

    except JWTError:
        return None


def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Long-lived Refresh Token generate karta hai (7 din validity)"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_refresh_token(refresh_token: str):
    """Refresh token ki validity aur type check karta hai"""
    try:
        payload = jwt.decode(
            refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        token_type = payload.get("type")
        if not user_id or token_type != "refresh":
            return None
        return payload
    except JWTError:
        return None


def create_password_reset_token(email: str) -> str:
    """15 minute ke liye valid reset token banata hai"""
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode = {"sub": email, "type": "password_reset", "exp": expire}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_password_reset_token(token: str) -> str | None:
    """Token verify karke email return karta hai"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "password_reset":
            return None
        return payload.get("sub")  # email
    except JWTError:
        return None
