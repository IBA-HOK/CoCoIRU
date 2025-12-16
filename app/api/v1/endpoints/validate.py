from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import verify_community_credentials, verify_gov_credentials
from db.session import get_db
from db import schemas

router = APIRouter()


@router.post("/validate", response_model=schemas.ValidationResponse)
def validate_credentials(
    payload: schemas.ValidationRequest,
    db: Session = Depends(get_db)
):
    """
    IDとパスワードを受け取って正しいか間違っているかを返す
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
        valid = verify_community_credentials(community_id, password, db)

    elif user_type == "gov":
        username = payload.username
        if not username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="'username' is required for gov users",
            )
        valid = verify_gov_credentials(username, password, db)

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="'user_type' must be either 'community' or 'gov'",
        )

    return schemas.ValidationResponse(valid=valid)