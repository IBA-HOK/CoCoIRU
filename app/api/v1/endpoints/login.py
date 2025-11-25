from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from datetime import timedelta, datetime

from app.core.security import require_token, create_access_token, verify_community_credentials, verify_gov_credentials, decode_access_token
from app.core.config import get_settings
from db.session import get_db
from db import schemas, crud

router = APIRouter()


@router.post("/login", response_model=schemas.TokenResponse)
def login(
    payload: schemas.TokenRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    ログイン: トークンを発行してHTTPOnly Cookieに保存
    """
    user_type = payload.user_type
    password = payload.password
    
    if user_type == "community":
        community_id = payload.community_id
        if not community_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="'community_id' is required for community users",
            )
        
        if not verify_community_credentials(community_id, password, db):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        
        settings = get_settings()
        expires_delta = timedelta(seconds=settings.access_token_expire_seconds)
        access_token = create_access_token(
            data={"sub": f"community:{community_id}"},
            role="community",
            expires_delta=expires_delta
        )
        role = "community"
        
    elif user_type == "gov":
        username = payload.username
        if not username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="'username' is required for gov users",
            )
        
        if not verify_gov_credentials(username, password, db):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        
        settings = get_settings()
        expires_delta = timedelta(seconds=settings.access_token_expire_seconds)
        access_token = create_access_token(
            data={"sub": f"gov:{username}"},
            role="gov",
            expires_delta=expires_delta
        )
        role = "gov"
        
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="'user_type' must be either 'community' or 'gov'",
        )
    
    # HTTPOnly Cookieにトークンを設定
    settings = get_settings()
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=settings.access_token_expire_seconds,
        secure=False,  # 開発環境用。本番ではTrue
        samesite="lax"
    )
    
    return schemas.TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.access_token_expire_seconds,
        role=role
    )


@router.post("/logout")
def logout(
    response: Response,
    token_data: dict = Depends(require_token),
    db: Session = Depends(get_db)
):
    """
    ログアウト: トークンをブラックリストに追加してCookieを削除
    """
    token = token_data.get("token")
    
    # トークンの有効期限を取得
    payload = decode_access_token(token)
    expires_at = datetime.fromtimestamp(payload.get("exp")).isoformat()
    
    # ブラックリストに追加
    crud.add_token_to_blacklist(db, token, expires_at)
    
    # Cookieを削除
    response.delete_cookie(key="access_token")
    
    return {"message": "Successfully logged out"}


@router.get("/me")
def get_current_user(token_data: dict = Depends(require_token)):
    """
    現在のログインユーザー情報を取得
    """
    return {
        "sub": token_data.get("sub"),
        "role": token_data.get("role")
    }