import sqlite3
import os
from datetime import datetime

def create_database_with_all_tables():
    """
    指定された全スキーマでSQLite3データベースとテーブルを作成します。
    PRIMARY KEY（主キー）および FOREIGN KEY（外部キー）制約を含みます。
    初期gov管理者アカウントも作成します。
    """
    db_name = 'database.db'
    
    try:
        # データベースに接続
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # --- SQLiteで外部キー制約を有効にする ---
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        print(f"データベース '{db_name}' に接続し、外部キー制約を有効にしました。")

        # --- テーブル作成（依存関係の順に作成）---

        # 1. 特記事項テーブル (Special_notes) 
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Special_notes (
            special_notes_id INTEGER PRIMARY KEY,
            notes_content_json TEXT,
            created_at TEXT
        );
        """)

        # 2. 支援品目テーブル (Items) 
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Items (
            items_id INTEGER PRIMARY KEY,
            item_name TEXT,
            unit TEXT,
            category TEXT,
            description TEXT
        );
        """)
        
        # 3. (追加) 避難所情報テーブル (Shelter_info) 
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Shelter_info (
            shelter_info INTEGER PRIMARY KEY,
            latitude REAL,
            longitude REAL,
            notes TEXT,
            created_at TEXT
        );
        """)

        # 3.5. 認証情報テーブル (Credential)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Credential (
            credential_id INTEGER PRIMARY KEY,
            hashed_password TEXT NOT NULL,
            created_at TEXT
        );
        """)

        # 4. メンバーテーブル (Members) - Special_notes に依存
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Members (
            member_id INTEGER PRIMARY KEY,
            special_notes_id INTEGER,
            created_at TEXT,
            FOREIGN KEY (special_notes_id) REFERENCES Special_notes (special_notes_id)
        );
        """)
        
        # 5. 要請内容テーブル (Request_content) - Items に依存
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

        # 6. コミュニティテーブル (Communities) - Members と Credential に依存
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Communities (
            community_id INTEGER PRIMARY KEY,
            member_id INTEGER,
            credential_id INTEGER NOT NULL UNIQUE,
            name TEXT,
            latitude REAL,
            longitude REAL,
            member_count INTEGER,
            created_at TEXT,
            FOREIGN KEY (member_id) REFERENCES Members (member_id),
            FOREIGN KEY (credential_id) REFERENCES Credential (credential_id)
        );
        """)

        # --- 新規: 物品追加申請テーブル (ItemAdditionRequests) - Communities に依存 ---
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ItemAdditionRequests (
            AddReq_id INTEGER PRIMARY KEY,
            Community_id INTEGER NOT NULL,
            Item_name TEXT NOT NULL,
            Item_unit TEXT,
            Reason TEXT,
            Timestamp TEXT NOT NULL,
            FOREIGN KEY (Community_id) REFERENCES Communities (community_id)
        );
        """)

        # 7. (追加) 避難所テーブル (Shelter) - Shelter_info と Communities に依存
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Shelter (
            shelter_id INTEGER PRIMARY KEY,
            shelter_info INTEGER,
            community_id INTEGER,
            created_at TEXT,
            
            -- 外部キー制約
            FOREIGN KEY (shelter_info) REFERENCES Shelter_info (shelter_info),
            FOREIGN KEY (community_id) REFERENCES Communities (community_id)
        );
        """)

        # 8. 支援物資要請テーブル (Support_Request) - Communities と Request_content に依存
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

        # 9. 政府ユーザーテーブル (GovUser) - Credential に依存
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS GovUser (
            gov_user_id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            credential_id INTEGER NOT NULL UNIQUE,
            email TEXT,
            full_name TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TEXT,
            FOREIGN KEY (credential_id) REFERENCES Credential (credential_id)
        );
        """)

        # 10. トークンブラックリストテーブル (TokenBlacklist)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS TokenBlacklist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT NOT NULL UNIQUE,
            blacklisted_at TEXT NOT NULL,
            expires_at TEXT NOT NULL
        );
        """)
        
        # トークン検索のためのインデックス
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_token ON TokenBlacklist(token);
        """)

        # 変更をコミット(保存)
        conn.commit()
        print("全テーブルが正常に作成または確認されました。")

        # --- 初期gov管理者アカウントの作成 ---
        create_initial_gov_admin(cursor, conn)

    except sqlite3.Error as e:
        print(f"データベース操作中にエラーが発生しました: {e}")
    
    finally:
        # データベース接続をクローズ
        if conn:
            conn.close()
            print("データベース接続をクローズしました。")


def create_initial_gov_admin(cursor, conn):
    """初期gov管理者アカウントを作成"""
    import bcrypt
    
    # 既存のgov_adminユーザーをチェック
    cursor.execute("SELECT gov_user_id FROM GovUser WHERE username = 'gov_admin'")
    existing_user = cursor.fetchone()
    
    if existing_user:
        print("初期gov管理者アカウント 'gov_admin' は既に存在します。")
        return
    
    # 環境変数からパスワードを取得、なければデフォルト値
    default_password = os.getenv("GOV_ADMIN_PASSWORD", "gov_admin_pass")
    
    # パスワードをハッシュ化
    password_bytes = default_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    hashed_password = hashed.decode('utf-8')
    
    # 現在時刻
    created_at = datetime.now().isoformat()
    
    # Credentialレコードを作成
    cursor.execute("""
    INSERT INTO Credential (hashed_password, created_at)
    VALUES (?, ?)
    """, (hashed_password, created_at))
    
    credential_id = cursor.lastrowid
    
    # GovUserレコードを作成
    cursor.execute("""
    INSERT INTO GovUser (username, credential_id, email, full_name, is_active, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, ("gov_admin", credential_id, "admin@gov.example.com", "Government Administrator", 1, created_at))
    
    conn.commit()
    print(f"初期gov管理者アカウント 'gov_admin' を作成しました。")
    print(f"  ユーザー名: gov_admin")
    print(f"  パスワード: {default_password}")
    print(f"  注意: 本番環境では環境変数 GOV_ADMIN_PASSWORD を設定してください。")


# --- スクリプトの実行 ---
if __name__ == "__main__":
    create_database_with_all_tables()