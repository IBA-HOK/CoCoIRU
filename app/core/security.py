from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import get_settings
from db.session import get_db
from db import crud

# Centralized OAuth2 dependency so every endpoint shares the same login gate.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")


def verify_community_credentials(community_id: int, password: str, db: Session) -> bool:
    """コミュニティIDとパスワードで認証"""
    community = crud.authenticate_community(db, community_id, password)
    return community is not None


def verify_gov_credentials(username: str, password: str, db: Session) -> bool:
    """govユーザー名とパスワードで認証"""
    gov_user = crud.authenticate_gov_user(db, username, password)
    return gov_user is not None


def create_access_token(data: dict, role: str, expires_delta: Optional[timedelta] = None) -> str:
    settings = get_settings()
    expire_delta = expires_delta or timedelta(seconds=settings.access_token_expire_seconds)
    expire = datetime.now(timezone.utc) + expire_delta
    to_encode = data.copy()
    to_encode.update({"exp": int(expire.timestamp()), "role": role})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def decode_access_token(token: str) -> dict:
    settings = get_settings()
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])


async def require_token(token: str = Depends(oauth2_scheme)) -> dict:
    """FastAPI dependency that enforces OAuth2 bearer authentication."""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = decode_access_token(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    subject = payload.get("sub")
    role = payload.get("role")
    if subject is None or role is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"sub": subject, "role": role}


async def require_gov_role(token_data: dict = Depends(require_token)) -> dict:
    """FastAPI dependency that requires gov role."""
    if token_data.get("role") != "gov":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Gov role required.",
        )
    return token_data
