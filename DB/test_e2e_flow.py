import sqlite3
import pytest

# --- スキーマ作成関数 (前のステップで作成したもの) ---
# テストのたびにこの関数を呼び出し、クリーンなDBをセットアップします。
def setup_schema(conn):
    """
    テスト用のインメモリDBにスキーマをセットアップする
    """
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # 1. Special_notes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Special_notes (
        special_notes_id INTEGER PRIMARY KEY,
        notes_content_json TEXT,
        created_at TEXT
    );
    """)
    # 2. Items
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Items (
        items_id INTEGER PRIMARY KEY,
        item_name TEXT,
        unit TEXT,
        category TEXT,
        description TEXT
    );
    """)
    # 3. Members
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Members (
        member_id INTEGER PRIMARY KEY,
        special_notes_id INTEGER,
        created_at TEXT,
        FOREIGN KEY (special_notes_id) REFERENCES Special_notes (special_notes_id)
    );
    """)
    # 4. Request_content
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Request_content (
        request_content_id INTEGER PRIMARY KEY,
        items_id INTEGER,
        other_note TEXT,
        number INTEGER,
        created_at TEXT,
        FOREIGN KEY (items_id) REFERENCES Items (items_id)
    );
    """)
    # 5. Communities
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Communities (
        community_id INTEGER PRIMARY KEY,
        member_id INTEGER,
        name TEXT,
        latitude REAL,
        longitude REAL,
        member_count INTEGER,
        created_at TEXT,
        FOREIGN KEY (member_id) REFERENCES Members (member_id)
    );
    """)
    # 6. Support_Request
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Support_Request (
        request_id INTEGER PRIMARY KEY,
        community_id INTEGER,
        request_content_id INTEGER,
        status TEXT,
        created_at TEXT,
        FOREIGN KEY (community_id) REFERENCES Communities (community_id),
        FOREIGN KEY (request_content_id) REFERENCES Request_content (request_content_id)
    );
    """)
    conn.commit()


# --- pytestフィクスチャ ---
@pytest.fixture(scope="function")
def db_conn():
    """
    テストのたびに、クリーンなインメモリDBへの接続を提供するフィクスチャ
    """
    # :memory: を使うと、ファイルを作らずメモリ上にDBを作成します
    conn = sqlite3.connect(":memory:")
    # スキーマ（テーブル定義）を作成
    setup_schema(conn)
    
    # テスト関数に接続を渡す (yield)
    yield conn
    
    # テスト終了後に接続を閉じる
    conn.close()


# --- テストケース ---

def test_e2e_community_request_flow(db_conn):
    """
    [E2Eテスト] 
    コミュニティが支援要請を作成する一連のフローをテストする
    """
    cursor = db_conn.cursor()
    
    # === データのセットアップ ===
    
    # 1. 特記事項を登録
    cursor.execute("INSERT INTO Special_notes (notes_content_json) VALUES ('{\"allergy\": \"none\"}')")
    note_id = cursor.lastrowid

    # 2. メンバーを登録
    cursor.execute("INSERT INTO Members (special_notes_id) VALUES (?)", (note_id,))
    member_id = cursor.lastrowid
    
    # 3. コミュニティを登録
    cursor.execute("INSERT INTO Communities (name, member_id, member_count) VALUES ('Test Community', ?, 10)", (member_id,))
    community_id = cursor.lastrowid

    # 4. 支援品目（水）を登録
    cursor.execute("INSERT INTO Items (item_name, unit, category) VALUES ('Water Bottle', 'bottle', 'drink')")
    item_id = cursor.lastrowid

    # === [実行] ビジネスロジックの実行 ===

    # 5. 要請内容（水, 100個）を作成
    cursor.execute("INSERT INTO Request_content (items_id, number) VALUES (?, 100)", (item_id,))
    content_id = cursor.lastrowid

    # 6. 支援要請を作成
    cursor.execute(
        "INSERT INTO Support_Request (community_id, request_content_id, status) VALUES (?, ?, 'pending')",
        (community_id, content_id)
    )
    request_id = cursor.lastrowid

    db_conn.commit()

    # === [検証] ===
    # 支援要請(Support_Request)を起点に、関連するテーブルをすべてJOINして、
    # 意図したデータが正しく紐付いているか確認する
    
    cursor.execute("""
        SELECT
            c.name,              -- コミュニティ名
            i.item_name,         -- 品目名
            rc.number,           -- 個数
            sr.status            -- 要請ステータス
        FROM Support_Request AS sr
        JOIN Communities AS c ON sr.community_id = c.community_id
        JOIN Request_content AS rc ON sr.request_content_id = rc.request_content_id
        JOIN Items AS i ON rc.items_id = i.items_id
        WHERE sr.request_id = ?
    """, (request_id,))
    
    result = cursor.fetchone()
    
    # 検証 (Assert)
    assert result is not None, "支援要請が見つかりません"
    assert result[0] == 'Test Community', "コミュニティ名が正しくありません"
    assert result[1] == 'Water Bottle', "品目名が正しくありません"
    assert result[2] == 100, "個数が正しくありません"
    assert result[3] == 'pending', "ステータスが正しくありません"
    print("\nE2Eフローテスト: 成功")


def test_foreign_key_violation(db_conn):
    """
    [整合性テスト]
    外部キー制約が正しく機能しているか（存在しないIDで登録しようとすると失敗するか）をテストする
    """
    cursor = db_conn.cursor()
    
    # 存在しない community_id (9999) と request_content_id (9999) を使って
    # 支援要請を作成しようとする
    
    # pytest.raises(...) は、ブロック内のコードが指定した例外(IntegrityError)を
    # 発生させることを期待する（発生すればテスト成功）
    with pytest.raises(sqlite3.IntegrityError, match="FOREIGN KEY constraint failed"):
        cursor.execute(
            "INSERT INTO Support_Request (community_id, request_content_id, status) VALUES (9999, 9999, 'failed')"
        )
    
    print("外部キー制約テスト: 成功")