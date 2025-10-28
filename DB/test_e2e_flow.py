import sqlite3
import pytest

# --- スキーマ作成関数 (全8テーブル) ---
def setup_schema(conn):
    """
    テスト用のインメモリDBに全8テーブルのスキーマをセットアップする
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
    # 3. Shelter_info
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Shelter_info (
        shelter_info INTEGER PRIMARY KEY,
        latitude REAL,
        longitude REAL,
        notes TEXT,
        created_at TEXT
    );
    """)
    # 4. Members
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Members (
        member_id INTEGER PRIMARY KEY,
        special_notes_id INTEGER,
        created_at TEXT,
        FOREIGN KEY (special_notes_id) REFERENCES Special_notes (special_notes_id)
    );
    """)
    # 5. Request_content
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
    # 6. Communities
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
    # 7. Shelter
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Shelter (
        shelter_id INTEGER PRIMARY KEY,
        shelter_info INTEGER,
        community_id INTEGER,
        created_at TEXT,
        FOREIGN KEY (shelter_info) REFERENCES Shelter_info (shelter_info),
        FOREIGN KEY (community_id) REFERENCES Communities (community_id)
    );
    """)
    # 8. Support_Request
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
    conn = sqlite3.connect(":memory:")
    setup_schema(conn)
    yield conn
    conn.close()


# --- テストケース ---

def test_e2e_shelter_and_request_flow(db_conn):
    """
    [E2Eテスト] 
    避難所登録と支援要請作成のフルフローをテストする
    """
    cursor = db_conn.cursor()
    
    # === [前提] データのセットアップ ===
    
    # 1. 特記事項、メンバー、品目を登録
    cursor.execute("INSERT INTO Special_notes (notes_content_json) VALUES ('{\"allergy\": \"none\"}')")
    note_id = cursor.lastrowid
    
    cursor.execute("INSERT INTO Members (special_notes_id) VALUES (?)", (note_id,))
    member_id = cursor.lastrowid

    cursor.execute("INSERT INTO Items (item_name, unit, category) VALUES ('Water Bottle', 'bottle', 'drink')")
    item_id = cursor.lastrowid

    # 2. コミュニティを登録
    cursor.execute("INSERT INTO Communities (name, member_id, member_count) VALUES ('Test Community', ?, 10)", (member_id,))
    community_id = cursor.lastrowid

    # 3. 避難所情報（場所）を登録
    cursor.execute("INSERT INTO Shelter_info (latitude, longitude, notes) VALUES (35.123, 137.456, 'Main Hall')")
    shelter_info_id = cursor.lastrowid

    # === [実行1] 避難所の登録 ===
    cursor.execute(
        "INSERT INTO Shelter (shelter_info, community_id) VALUES (?, ?)",
        (shelter_info_id, community_id)
    )
    shelter_id = cursor.lastrowid

    # === [実行2] 支援要請の作成 ===
    
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

    # === [検証1] 支援要請の確認 ===
    cursor.execute("""
        SELECT c.name, i.item_name, rc.number, sr.status
        FROM Support_Request AS sr
        JOIN Communities AS c ON sr.community_id = c.community_id
        JOIN Request_content AS rc ON sr.request_content_id = rc.request_content_id
        JOIN Items AS i ON rc.items_id = i.items_id
        WHERE sr.request_id = ?
    """, (request_id,))
    
    request_result = cursor.fetchone()
    
    assert request_result is not None, "支援要請が見つかりません"
    assert request_result[0] == 'Test Community', "支援要請のコミュニティ名が違います"
    assert request_result[1] == 'Water Bottle', "支援要請の品目名が違います"
    assert request_result[2] == 100, "支援要請の個数が違います"
    print("\nE2Eテスト(1/2): 支援要請フロー 成功")

    # === [検証2] 避難所登録の確認 ===
    cursor.execute("""
        SELECT c.name, si.latitude, si.longitude, si.notes
        FROM Shelter AS s
        JOIN Communities AS c ON s.community_id = c.community_id
        JOIN Shelter_info AS si ON s.shelter_info = si.shelter_info
        WHERE s.shelter_id = ?
    """, (shelter_id,))
    
    shelter_result = cursor.fetchone()
    
    assert shelter_result is not None, "避難所が見つかりません"
    assert shelter_result[0] == 'Test Community', "避難所のコミュニティ名が違います"
    assert shelter_result[1] == 35.123, "避難所の緯度が違います"
    assert shelter_result[3] == 'Main Hall', "避難所の備考が違います"
    print("E2Eテスト(2/2): 避難所登録フロー 成功")


def test_support_request_foreign_key_violation(db_conn):
    """
    [整合性テスト]
    Support_Requestテーブルの外部キー制約が機能するかテスト
    """
    with pytest.raises(sqlite3.IntegrityError, match="FOREIGN KEY constraint failed"):
        # 存在しない community_id (9999) で登録
        db_conn.execute(
            "INSERT INTO Support_Request (community_id, request_content_id, status) VALUES (9999, 9999, 'failed')"
        )
    print("\n外部キー制約テスト(1/2): Support_Request 成功")


def test_shelter_foreign_key_violation(db_conn):
    """
    [整合性テスト]
    Shelterテーブルの外部キー制約が機能するかテスト
    """
    with pytest.raises(sqlite3.IntegrityError, match="FOREIGN KEY constraint failed"):
        # 存在しない community_id (8888) と shelter_info (8888) で登録
        db_conn.execute(
            "INSERT INTO Shelter (shelter_info, community_id) VALUES (8888, 8888)"
        )
    print("外部キー制約テスト(2/2): Shelter 成功")