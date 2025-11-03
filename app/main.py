from fastapi import FastAPI, Request 
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse 
from sqlalchemy.exc import IntegrityError 
from db.session import engine
from db import models

from app.api.v1.api import api_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CoCoIRU API",
    version="1.0.0"
)

@app.exception_handler(IntegrityError)
async def integrity_error_exception_handler(request: Request, exc: IntegrityError):
    """
    SQLAlchemyの外部キー制約違反(IntegrityError)をキャッチし、
    409 Conflict (または 400 Bad Request) を返す。
    """
    print(f"(!) データベース整合性エラー発生: {exc.orig}") # サーバーログ
    return JSONResponse(
        status_code=409, # 409 Conflict がセマンティック的に適切
        content={
            "detail": f"Database integrity error. A referenced resource may not exist. Error: {exc.orig}"
        },
    )

app.include_router(api_router, prefix="/api/v1")



@app.get("/health", tags=["Server Health"])
def health_check():
    return {"status": "ok", "message": "Welcome to CoCoIRU API"}