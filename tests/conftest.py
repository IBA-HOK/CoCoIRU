import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

# --- アプリケーション本体とDB関連をインポート ---
# (PYTHONPATHが通っている前提。通ってない場合は sys.path.append で調整)
from app.main import app
from db.session import Base, get_db

# --- テスト用データベース設定 ---
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Ensure SQLite foreign key enforcement is active for the test engine
@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    try:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
    except Exception:
        pass

# --- テスト用フィクスチャ ---

@pytest.fixture(scope="session")
def db_engine():
    """
    テストDB用のEngineを作成し、全テーブルを作成
    """
    # テストDB（インメモリ）に全テーブルを作成
    Base.metadata.create_all(bind=engine)
    yield engine
    # テスト終了後 (不要だが念のため)
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(db_engine):
    """
    各テスト関数用のDBセッション (トランザクション) を提供
    テスト終了時にロールバックしてクリーンな状態に戻す
    """
    connection = db_engine.connect()

    # トランザクションを開始
    transaction = connection.begin()

    # セッションを作成
    session = TestingSessionLocal(bind=connection)

    yield session

    # セッションをクローズ
    session.close()

    # トランザクションをロールバック (テストデータをリセット)
    # It's possible the transaction was already rolled back (e.g. due to an IntegrityError
    # triggered inside the app). Guard against that to avoid SAWarning.
    # Only rollback if the transaction is still active. Calling rollback on a
    # de-associated transaction triggers SAWarning; check attribute to avoid it.
    try:
        is_active = getattr(transaction, "is_active", None)
    except Exception:
        is_active = None

    if is_active:
        transaction.rollback()
    
    # 接続をクローズ
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    """
    テスト用のFastAPI TestClientを提供
    APIが 'get_db' を呼んだ際に、テスト用DBセッション (db_session) を返すようオーバーライド
    """

    def override_get_db():
        """
        FastAPIの 'Depends(get_db)' をオーバーライドし、
        テスト用セッションを注入する関数
        """
        try:
            yield db_session
        finally:
            # db_sessionのクローズはフィクスチャ側で行う
            pass

    # FastAPIアプリの依存関係 (get_db) をテスト用 (override_get_db) に上書き
    app.dependency_overrides[get_db] = override_get_db

    # オーバーライドしたアプリでTestClientを作成
    with TestClient(app) as c:
        yield c
    
    # テスト終了後、オーバーライドを元に戻す
    app.dependency_overrides.clear()