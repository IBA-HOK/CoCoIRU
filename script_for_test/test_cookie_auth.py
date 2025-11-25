#!/usr/bin/env python3
"""
Cookie認証とブラックリスト機能のテストスクリプト
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

def print_separator():
    print("\n" + "="*60 + "\n")

def test_gov_login():
    """Gov管理者ログインテスト"""
    print("🔑 Gov管理者ログインテスト")
    
    session = requests.Session()
    
    response = session.post(
        f"{BASE_URL}/login/login",
        json={
            "user_type": "gov",
            "username": "gov_admin",
            "password": "gov_admin_pass"
        }
    )
    
    print(f"ステータスコード: {response.status_code}")
    print(f"レスポンス: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print(f"Cookieが設定されました: {'access_token' in session.cookies}")
    
    return session

def test_me_endpoint(session):
    """ログインユーザー情報取得テスト"""
    print("👤 ログインユーザー情報取得テスト")
    
    # デバッグ: Cookieを表示
    print(f"送信するCookie: {dict(session.cookies)}")
    
    response = session.get(f"{BASE_URL}/login/me")
    
    print(f"ステータスコード: {response.status_code}")
    print(f"レスポンス: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    return response.status_code == 200

def test_gov_only_access(session):
    """Gov専用エンドポイントアクセステスト"""
    print("🔒 Gov専用エンドポイントアクセステスト")
    
    response = session.get(f"{BASE_URL}/communities/")
    
    print(f"ステータスコード: {response.status_code}")
    if response.status_code == 200:
        print(f"コミュニティ数: {len(response.json())}")
    else:
        print(f"エラー: {response.json()}")
    
    return response.status_code == 200

def test_logout(session):
    """ログアウトテスト"""
    print("🚪 ログアウトテスト")
    
    response = session.post(f"{BASE_URL}/login/logout")
    
    print(f"ステータスコード: {response.status_code}")
    print(f"レスポンス: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    return response.status_code == 200

def test_access_after_logout(session):
    """ログアウト後のアクセステスト (ブラックリスト確認)"""
    print("⛔ ログアウト後のアクセステスト")
    
    response = session.get(f"{BASE_URL}/login/me")
    
    print(f"ステータスコード: {response.status_code}")
    print(f"レスポンス: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    return response.status_code == 401

def main():
    print("=" * 60)
    print("Cookie認証とブラックリスト機能のテスト")
    print("=" * 60)
    
    try:
        # 1. ログイン
        print_separator()
        session = test_gov_login()
        
        # 2. ログインユーザー情報取得
        print_separator()
        if not test_me_endpoint(session):
            print("❌ /me エンドポイントアクセス失敗")
            return
        
        # 3. Gov専用エンドポイントアクセス
        print_separator()
        if not test_gov_only_access(session):
            print("❌ Gov専用エンドポイントアクセス失敗")
            return
        
        # 4. ログアウト
        print_separator()
        if not test_logout(session):
            print("❌ ログアウト失敗")
            return
        
        # 5. ログアウト後のアクセス (ブラックリストによるリジェクト確認)
        print_separator()
        if not test_access_after_logout(session):
            print("❌ ブラックリストが機能していません")
            return
        
        print_separator()
        print("✅ すべてのテストが成功しました!")
        
    except requests.exceptions.ConnectionError:
        print("❌ サーバーに接続できません。APIサーバーが起動しているか確認してください。")
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")

if __name__ == "__main__":
    main()
