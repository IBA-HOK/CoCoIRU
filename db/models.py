# from .database import Base  <- 変更前
from db.session import Base  # <- 変更後
from sqlalchemy import Column, Integer, String, REAL, TEXT, ForeignKey
from sqlalchemy.orm import relationship

# ... (全8テーブルのモデル定義) ...
class Items(Base):
    __tablename__ = "Items"
    