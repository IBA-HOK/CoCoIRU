from fastapi import APIRouter, Depends

from app.core.security import oauth2_scheme

router = APIRouter()

@router.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}