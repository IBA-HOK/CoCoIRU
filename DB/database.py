import sqlite3

def create_database_with_foreign_keys():
    db_name = 'database.db'
    
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        print(f"データベース '{db_name}' に接続し、外部キー制約を有効にしました。")

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

        # 3. メンバーテーブル (Members) - Special_notes に依存
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Members (
            member_id INTEGER PRIMARY KEY,
            special_notes_id INTEGER,
            created_at TEXT,
            
            -- 外部キー制約: special_notes_id は Special_notes テーブルを参照
            FOREIGN KEY (special_notes_id) REFERENCES Special_notes (special_notes_id)
        );
        """)
        
        # 4. 要請内容テーブル (Request_content) - Items に依存
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Request_content (
            request_content_id INTEGER PRIMARY KEY,
            items_id INTEGER,
            other_note TEXT,
            number INTEGER,
            created_at TEXT,
            
            -- 外部キー制約: items_id は Items テーブルを参照
            FOREIGN KEY (items_id) REFERENCES Items (items_id)
        );
        """)

        # 5. コミュニティテーブル (Communities) - Members に依存
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Communities (
            community_id INTEGER PRIMARY KEY,
            member_id INTEGER,
            name TEXT,
            latitude REAL,
            longitude REAL,
            member_count INTEGER,
            created_at TEXT,
            
            -- 外部キー制約: member_id は Members テーブルを参照
            FOREIGN KEY (member_id) REFERENCES Members (member_id)
        );
        """)

        # 6. 支援物資要請テーブル (Support_Request) - Communities と Request_content に依存
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Support_Request (
            request_id INTEGER PRIMARY KEY,
            community_id INTEGER,
            request_content_id INTEGER,
            status TEXT,
            created_at TEXT,
            
            -- 外部キー制約: community_id は Communities テーブルを参照
            FOREIGN KEY (community_id) REFERENCES Communities (community_id),
            
            -- 外部キー制約: request_content_id は Request_content テーブルを参照
            FOREIGN KEY (request_content_id) REFERENCES Request_content (request_content_id)
        );
        """)

        # 変更をコミット（保存）
        conn.commit()
        print("テーブルが正常に作成または確認されました。")

    except sqlite3.Error as e:
        print(f"データベース操作中にエラーが発生しました: {e}")
    
    finally:
        # データベース接続をクローズ
        if conn:
            conn.close()
            print("データベース接続をクローズしました。")

# --- スクリプトの実行 ---
if __name__ == "__main__":
    create_database_with_foreign_keys()