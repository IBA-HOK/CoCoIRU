from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# プロジェクトルートにある 'database.db' を参照
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SQLite does not enforce foreign key constraints by default. Enable them on connect
@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    # sqlite3 DB-API connection
    try:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
    except Exception:
        # If not sqlite or cannot set PRAGMA, ignore silently
        pass
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()