import sqlite3

def create_database_with_all_tables():
    """
    指定された全スキーマでSQLite3データベースとテーブルを作成します。
    PRIMARY KEY（主キー）および FOREIGN KEY（外部キー）制約を含みます。
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

        # 6. コミュニティテーブル (Communities) - Members に依存
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

        # 変更をコミット（保存）
        conn.commit()
        print("全8テーブルが正常に作成または確認されました。")

    except sqlite3.Error as e:
        print(f"データベース操作中にエラーが発生しました: {e}")
    
    finally:
        # データベース接続をクローズ
        if conn:
            conn.close()
            print("データベース接続をクローズしました。")

# --- スクリプトの実行 ---
if __name__ == "__main__":
    create_database_with_all_tables()