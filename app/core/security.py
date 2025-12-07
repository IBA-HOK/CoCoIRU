from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status, Cookie, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import get_settings
from db.session import get_db
from db import crud

# Centralized OAuth2 dependency so every endpoint shares the same login gate.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token", auto_error=False)


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


async def require_token(
    request: Request,
    authorization: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> dict:
    """FastAPI dependency that enforces OAuth2 bearer authentication.
    Checks cookie first, then Authorization header. Also validates against blacklist.
    """
    settings = get_settings()
    
    # 開発モードの場合は認証をバイパス
    if settings.dev_mode:
        print("DEBUG: DEV_MODE is enabled, bypassing authentication")
        return {"sub": "dev_user", "role": "admin", "token": "dev_bypass"}
    
    # 同一ポート(8000)からのリクエストは素通し
    client_host = request.client.host if request.client else None
    client_port = request.client.port if request.client else None
    server_port = request.url.port or 8000  # デフォルトは8000
    
    if client_host in ["127.0.0.1", "localhost", "::1"] and client_port == server_port:
        print(f"DEBUG: Same-port request from {client_host}:{client_port}, bypassing authentication")
        return {"sub": "localhost", "role": "admin", "token": "localhost_bypass"}
    
    # プリフライトOPTIONSは認証ヘッダーを持たないためスキップ
    if request.method == "OPTIONS":
        print("DEBUG: OPTIONS preflight request - skipping auth check")
        return {"sub": "preflight", "role": "preflight", "token": ""}

    # 生のAuthorizationヘッダーとメソッドを表示（デバッグ用）
    raw_auth = request.headers.get('authorization')
    print(f"DEBUG: method={request.method}, raw_authorization={raw_auth}")

    # Cookie優先でトークン取得
    access_token = request.cookies.get("access_token")
    token = access_token or authorization
    
    print(f"DEBUG: Cookie={access_token[:20] if access_token else None}, Auth={authorization[:20] if authorization else None}, Token={token[:20] if token else None}")
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # ブラックリストチェック
    if crud.is_token_blacklisted(db, token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
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

    return {"sub": subject, "role": role, "token": token}


async def require_gov_role(token_data: dict = Depends(require_token)) -> dict:
    """FastAPI dependency that requires gov role."""
    # localhostからのリクエストはadmin権限で素通し
    if token_data.get("role") == "admin":
        return token_data
    
    if token_data.get("role") != "gov":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Gov role required.",
        )
    return token_data
