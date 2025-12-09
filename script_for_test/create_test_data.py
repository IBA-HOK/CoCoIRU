#!/usr/bin/env python3
"""
CoCoIRU API テストデータ作成スクリプト

このスクリプトは、開発・テスト用の初期データを作成します。
- Gov管理者（自動作成済み）
- コミュニティユーザー
- 支援品目（Items）
- 支援要請（Support Requests）
- その他関連データ
"""

import requests
import json
import sys
from datetime import datetime

# API設定
BASE_URL = "http://127.0.0.1:8000/api/v1"
GOV_USERNAME = "gov_admin"
GOV_PASSWORD = "gov_admin_pass"

# カラー出力用
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")

def get_gov_token():
    """Gov管理者のトークンを取得"""
    print_info("Gov管理者トークンを取得中...")
    response = requests.post(
        f"{BASE_URL}/token",
        json={
            "user_type": "gov",
            "username": GOV_USERNAME,
            "password": GOV_PASSWORD
        }
    )
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print_success("Gov管理者トークン取得成功")
        return token
    else:
        print_error(f"Gov管理者トークン取得失敗: {response.text}")
        return None

def create_special_notes(token, notes_list):
    """Special Notesを作成"""
    print_info(f"{len(notes_list)}件のSpecial Notesを作成中...")
    headers = {"Authorization": f"Bearer {token}"}
    created_ids = []
    
    for note in notes_list:
        response = requests.post(
            f"{BASE_URL}/special_notes/",
            headers=headers,
            json=note
        )
        if response.status_code == 200:
            special_notes_id = response.json()["special_notes_id"]
            created_ids.append(special_notes_id)
            print_success(f"Special Note ID {special_notes_id} 作成")
        else:
            print_error(f"Special Note作成失敗: {response.status_code} - {response.text}")
    
    return created_ids

def create_members(token, special_notes_ids):
    """Membersを作成"""
    print_info(f"{len(special_notes_ids)}件のMembersを作成中...")
    headers = {"Authorization": f"Bearer {token}"}
    created_ids = []
    
    for special_notes_id in special_notes_ids:
        response = requests.post(
            f"{BASE_URL}/members/",
            headers=headers,
            json={
                "special_notes_id": special_notes_id,
                "created_at": datetime.now().isoformat()
            }
        )
        if response.status_code == 200:
            member_id = response.json()["member_id"]
            created_ids.append(member_id)
            print_success(f"Member ID {member_id} 作成")
        else:
            print_error(f"Member作成失敗: {response.text}")
    
    return created_ids

def create_communities(member_ids, community_data):
    """Communitiesを作成（認証不要）"""
    print_info(f"{len(community_data)}件のCommunitiesを作成中...")
    created = []
    
    for i, (member_id, data) in enumerate(zip(member_ids, community_data)):
        data_with_member = {**data, "member_id": member_id}
        response = requests.post(
            f"{BASE_URL}/communities/",
            json=data_with_member
        )
        if response.status_code == 200:
            community = response.json()
            created.append(community)
            print_success(f"Community ID {community['community_id']} ({data['name']}) 作成")
        else:
            print_error(f"Community作成失敗: {response.text}")
    
    return created

def create_items(token, items_list):
    """Itemsを作成"""
    print_info(f"{len(items_list)}件のItemsを作成中...")
    headers = {"Authorization": f"Bearer {token}"}
    created_ids = []
    
    for item in items_list:
        response = requests.post(
            f"{BASE_URL}/items/",
            headers=headers,
            json=item
        )
        if response.status_code == 200:
            item_id = response.json()["items_id"]
            created_ids.append(item_id)
            print_success(f"Item ID {item_id} ({item['item_name']}) 作成")
        else:
            print_error(f"Item作成失敗: {response.status_code} - {response.text}")
    
    return created_ids

def create_request_contents(token, items_ids, request_data):
    """Request Contentsを作成"""
    print_info(f"{len(request_data)}件のRequest Contentsを作成中...")
    headers = {"Authorization": f"Bearer {token}"}
    created_ids = []
    
    for data in request_data:
        response = requests.post(
            f"{BASE_URL}/request_content/",
            headers=headers,
            json=data
        )
        if response.status_code == 200:
            request_content_id = response.json()["request_content_id"]
            created_ids.append(request_content_id)
            print_success(f"Request Content ID {request_content_id} 作成")
        else:
            print_error(f"Request Content作成失敗: {response.text}")
    
    return created_ids

def create_support_requests(token, community_ids, request_content_ids, support_data):
    """Support Requestsを作成"""
    print_info(f"{len(support_data)}件のSupport Requestsを作成中...")
    headers = {"Authorization": f"Bearer {token}"}
    created_ids = []
    
    for data in support_data:
        response = requests.post(
            f"{BASE_URL}/support_requests/",
            headers=headers,
            json=data
        )
        if response.status_code == 200:
            request_id = response.json()["request_id"]
            created_ids.append(request_id)
            print_success(f"Support Request ID {request_id} 作成")
        else:
            print_error(f"Support Request作成失敗: {response.text}")
    
    return created_ids

def create_shelter_info(token, shelter_info_list):
    """Shelter Infoを作成"""
    print_info(f"{len(shelter_info_list)}件のShelter Infoを作成中...")
    headers = {"Authorization": f"Bearer {token}"}
    created_ids = []
    
    for info in shelter_info_list:
        response = requests.post(
            f"{BASE_URL}/shelter_info/",
            headers=headers,
            json=info
        )
        if response.status_code == 200:
            shelter_info_id = response.json()["shelter_info"]
            created_ids.append(shelter_info_id)
            print_success(f"Shelter Info ID {shelter_info_id} 作成")
        else:
            print_error(f"Shelter Info作成失敗: {response.text}")
    
    return created_ids

def main():
    print("=" * 60)
    print("CoCoIRU API テストデータ作成スクリプト")
    print("=" * 60)
    print()
    
    # Gov管理者トークン取得
    gov_token = get_gov_token()
    if not gov_token:
        print_error("Gov管理者トークンが取得できませんでした。処理を中断します。")
        sys.exit(1)
    
    print()
    
    # 1. Special Notesを作成
    print("【1/7】Special Notes作成")
    special_notes_data = [
        {"notes_content_json": json.dumps({"note": "アレルギー: 小麦"}), "created_at": datetime.now().isoformat()},
        {"notes_content_json": json.dumps({"note": "車椅子利用者あり"}), "created_at": datetime.now().isoformat()},
        {"notes_content_json": json.dumps({"note": "乳幼児が多い"}), "created_at": datetime.now().isoformat()},
        {"notes_content_json": json.dumps({"note": "高齢者が多い"}), "created_at": datetime.now().isoformat()},
    ]
    special_notes_ids = create_special_notes(gov_token, special_notes_data)
    print()
    
    # 2. Membersを作成
    print("【2/7】Members作成")
    member_ids = create_members(gov_token, special_notes_ids)
    print()
    
    # 3. Communitiesを作成
    print("【3/7】Communities作成")
    communities_data = [
        {
            "name": "北区避難所A",
            "password": "community001",
            "latitude": 35.7536,
            "longitude": 139.7136,
            "member_count": 45,
            "created_at": datetime.now().isoformat()
        },
        {
            "name": "中央区避難所B",
            "password": "community002",
            "latitude": 35.6762,
            "longitude": 139.7649,
            "member_count": 82,
            "created_at": datetime.now().isoformat()
        },
        {
            "name": "南区避難所C",
            "password": "community003",
            "latitude": 35.6580,
            "longitude": 139.7016,
            "member_count": 63,
            "created_at": datetime.now().isoformat()
        },
        {
            "name": "西区避難所D",
            "password": "community004",
            "latitude": 35.6938,
            "longitude": 139.5703,
            "member_count": 51,
            "created_at": datetime.now().isoformat()
        },
    ]
    communities = create_communities(member_ids, communities_data)
    community_ids = [c["community_id"] for c in communities]
    print()
    
    # 4. Itemsを作成
    print("【4/7】Items作成")
    items_data = [
        {"item_name": "飲料水", "unit": "本", "category": "飲料", "description": "500mlペットボトル"},
        {"item_name": "米", "unit": "kg", "category": "食料", "description": "白米"},
        {"item_name": "缶詰", "unit": "個", "category": "食料", "description": "各種缶詰"},
        {"item_name": "毛布", "unit": "枚", "category": "生活用品", "description": "防寒用毛布"},
        {"item_name": "紙おむつ", "unit": "パック", "category": "衛生用品", "description": "乳幼児用"},
        {"item_name": "マスク", "unit": "箱", "category": "衛生用品", "description": "使い捨てマスク50枚入り"},
        {"item_name": "懐中電灯", "unit": "個", "category": "生活用品", "description": "電池式"},
        {"item_name": "乾電池", "unit": "パック", "category": "生活用品", "description": "単3形4本入り"},
        {"item_name": "簡易トイレ", "unit": "セット", "category": "衛生用品", "description": "災害用"},
        {"item_name": "レトルト食品", "unit": "個", "category": "食料", "description": "カレー、シチューなど"},
    ]
    items_ids = create_items(gov_token, items_data)
    print()
    
    # 5. Request Contentsを作成
    print("【5/7】Request Contents作成")
    request_contents_data = [
        {"items_id": items_ids[0], "number": 200, "other_note": "急募", "created_at": datetime.now().isoformat()},
        {"items_id": items_ids[1], "number": 50, "other_note": None, "created_at": datetime.now().isoformat()},
        {"items_id": items_ids[3], "number": 100, "other_note": "寒さ対策", "created_at": datetime.now().isoformat()},
        {"items_id": items_ids[4], "number": 30, "other_note": "Mサイズ希望", "created_at": datetime.now().isoformat()},
        {"items_id": items_ids[5], "number": 50, "other_note": None, "created_at": datetime.now().isoformat()},
        {"items_id": items_ids[2], "number": 150, "other_note": None, "created_at": datetime.now().isoformat()},
        {"items_id": items_ids[6], "number": 20, "other_note": None, "created_at": datetime.now().isoformat()},
        {"items_id": items_ids[9], "number": 100, "other_note": None, "created_at": datetime.now().isoformat()},
    ]
    request_content_ids = create_request_contents(gov_token, items_ids, request_contents_data)
    print()
    
    # 6. Support Requestsを作成
    print("【6/7】Support Requests作成")
    support_requests_data = [
        {"community_id": community_ids[0], "request_content_id": request_content_ids[0], "status": "pending", "created_at": datetime.now().isoformat()},
        {"community_id": community_ids[0], "request_content_id": request_content_ids[1], "status": "pending", "created_at": datetime.now().isoformat()},
        {"community_id": community_ids[1], "request_content_id": request_content_ids[2], "status": "approved", "created_at": datetime.now().isoformat()},
        {"community_id": community_ids[1], "request_content_id": request_content_ids[3], "status": "pending", "created_at": datetime.now().isoformat()},
        {"community_id": community_ids[2], "request_content_id": request_content_ids[4], "status": "completed", "created_at": datetime.now().isoformat()},
        {"community_id": community_ids[2], "request_content_id": request_content_ids[5], "status": "pending", "created_at": datetime.now().isoformat()},
        {"community_id": community_ids[3], "request_content_id": request_content_ids[6], "status": "pending", "created_at": datetime.now().isoformat()},
        {"community_id": community_ids[3], "request_content_id": request_content_ids[7], "status": "approved", "created_at": datetime.now().isoformat()},
    ]
    support_request_ids = create_support_requests(gov_token, community_ids, request_content_ids, support_requests_data)
    print()
    
    # 7. Shelter Infoを作成
    print("【7/7】Shelter Info作成")
    shelter_info_data = [
        {"latitude": 35.7536, "longitude": 139.7136, "notes": "体育館、収容人数200人", "created_at": datetime.now().isoformat()},
        {"latitude": 35.6762, "longitude": 139.7649, "notes": "小学校、収容人数150人", "created_at": datetime.now().isoformat()},
        {"latitude": 35.6580, "longitude": 139.7016, "notes": "公民館、収容人数100人", "created_at": datetime.now().isoformat()},
    ]
    shelter_info_ids = create_shelter_info(gov_token, shelter_info_data)
    print()
    
    # 完了メッセージ
    print("=" * 60)
    print_success("テストデータ作成完了!")
    print("=" * 60)
    print()
    print("作成されたデータ:")
    print(f"  - Special Notes: {len(special_notes_ids)}件")
    print(f"  - Members: {len(member_ids)}件")
    print(f"  - Communities: {len(community_ids)}件")
    print(f"  - Items: {len(items_ids)}件")
    print(f"  - Request Contents: {len(request_content_ids)}件")
    print(f"  - Support Requests: {len(support_request_ids)}件")
    print(f"  - Shelter Info: {len(shelter_info_ids)}件")
    print()
    print("コミュニティアカウント情報:")
    for i, community in enumerate(communities, 1):
        print(f"  {i}. {community['name']}")
        print(f"     ID: {community['community_id']}")
        print(f"     パスワード: {communities_data[i-1]['password']}")
    print()
    print("Gov管理者アカウント:")
    print(f"  ユーザー名: {GOV_USERNAME}")
    print(f"  パスワード: {GOV_PASSWORD}")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print_warning("処理が中断されました")
        sys.exit(1)
    except Exception as e:
        print()
        print_error(f"エラーが発生しました: {str(e)}")
        sys.exit(1)
