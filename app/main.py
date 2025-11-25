from fastapi import FastAPI, Request 
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse 
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError 
from db.session import engine
from db import models

from app.api.v1.api import api_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CoCoIRU API",
    version="1.0.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 開発環境用。本番環境では特定のオリジンを指定してください
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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