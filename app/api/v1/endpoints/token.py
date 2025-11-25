from datetime import timedelta
from typing import Any, Dict

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import create_access_token, verify_community_credentials, verify_gov_credentials
from db.session import get_db
from db import schemas

router = APIRouter(tags=["Auth"])


@router.post("", response_model=schemas.TokenResponse)
def issue_token(payload: schemas.TokenRequest, db: Session = Depends(get_db)):
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
                headers={"WWW-Authenticate": "Bearer"},
            )

        settings = get_settings()
        expires_delta = timedelta(seconds=settings.access_token_expire_seconds)
        access_token = create_access_token(
            data={"sub": f"community:{community_id}"},
            role="community",
            expires_delta=expires_delta
        )

        return schemas.TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_seconds,
            role="community"
        )

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
                headers={"WWW-Authenticate": "Bearer"},
            )

        settings = get_settings()
        expires_delta = timedelta(seconds=settings.access_token_expire_seconds)
        access_token = create_access_token(
            data={"sub": f"gov:{username}"},
            role="gov",
            expires_delta=expires_delta
        )

        return schemas.TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_seconds,
            role="gov"
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="'user_type' must be either 'community' or 'gov'",
        )
