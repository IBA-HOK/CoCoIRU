#!/bin/bash

# RBAC実装のテストスクリプト

BASE_URL="http://127.0.0.1:8000/api/v1"

echo "=== CoCoIRU RBAC実装テスト ==="
echo ""

# 1. Gov管理者としてトークン取得
echo "1. Gov管理者としてトークン取得"
GOV_RESPONSE=$(curl -s -X POST "$BASE_URL/token" \
  -H "Content-Type: application/json" \
  -d '{"user_type": "gov", "username": "gov_admin", "password": "gov_admin_pass"}')

echo "$GOV_RESPONSE" | python3 -m json.tool
GOV_TOKEN=$(echo "$GOV_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
echo ""

# 2. Special Notesを作成（前提データ）
echo "2. Special Notesを作成（前提データ）"
curl -s -X POST "$BASE_URL/special_notes/" \
  -H "Authorization: Bearer $GOV_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"notes_content_json": "{\"test\": \"data\"}"}' | python3 -m json.tool
echo ""

# 3. Membersを作成（前提データ）
echo "3. Membersを作成（前提データ）"
curl -s -X POST "$BASE_URL/members/" \
  -H "Authorization: Bearer $GOV_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"special_notes_id": 1}' | python3 -m json.tool
echo ""

# 4. コミュニティを作成（認証不要）
echo "4. コミュニティを作成（認証不要）"
curl -s -X POST "$BASE_URL/communities/" \
  -H "Content-Type: application/json" \
  -d '{"member_id": 1, "name": "テストコミュニティ", "password": "test_pass"}' | python3 -m json.tool
echo ""

# 5. コミュニティユーザーとしてトークン取得
echo "5. コミュニティユーザーとしてトークン取得"
COMMUNITY_RESPONSE=$(curl -s -X POST "$BASE_URL/token" \
  -H "Content-Type: application/json" \
  -d '{"user_type": "community", "community_id": 1, "password": "test_pass"}')

echo "$COMMUNITY_RESPONSE" | python3 -m json.tool
COMMUNITY_TOKEN=$(echo "$COMMUNITY_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
echo ""

# 6. Gov専用: 全コミュニティ一覧取得（Govトークン）
echo "6. Gov専用: 全コミュニティ一覧取得（Govトークンで成功）"
curl -s -X GET "$BASE_URL/communities/" \
  -H "Authorization: Bearer $GOV_TOKEN" | python3 -m json.tool
echo ""

# 7. Gov専用: 全コミュニティ一覧取得（Communityトークン）
echo "7. Gov専用: 全コミュニティ一覧取得（Communityトークンで403エラー）"
curl -s -X GET "$BASE_URL/communities/" \
  -H "Authorization: Bearer $COMMUNITY_TOKEN" | python3 -m json.tool
echo ""

# 8. 個別リソース: コミュニティユーザーでもアクセス可能
echo "8. 個別リソース: コミュニティユーザーでもアクセス可能"
curl -s -X GET "$BASE_URL/communities/1" \
  -H "Authorization: Bearer $COMMUNITY_TOKEN" | python3 -m json.tool
echo ""

# 9. Itemsを作成してSupport Requestを作成
echo "9. Itemsを作成"
curl -s -X POST "$BASE_URL/items/" \
  -H "Authorization: Bearer $COMMUNITY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"item_name": "水", "unit": "本", "category": "飲料", "description": "500ml"}' | python3 -m json.tool
echo ""

echo "10. Request Contentを作成"
curl -s -X POST "$BASE_URL/request_content/" \
  -H "Authorization: Bearer $COMMUNITY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"items_id": 1, "number": 100}' | python3 -m json.tool
echo ""

echo "11. Support Requestを作成（Communityユーザー）"
curl -s -X POST "$BASE_URL/support_requests/" \
  -H "Authorization: Bearer $COMMUNITY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"community_id": 1, "request_content_id": 1, "status": "pending"}' | python3 -m json.tool
echo ""

# 10. Gov専用: 全Support Request一覧取得
echo "12. Gov専用: 全Support Request一覧取得（Govトークンで成功）"
curl -s -X GET "$BASE_URL/support_requests/" \
  -H "Authorization: Bearer $GOV_TOKEN" | python3 -m json.tool
echo ""

echo "13. Gov専用: 全Support Request一覧取得（Communityトークンで403エラー）"
curl -s -X GET "$BASE_URL/support_requests/" \
  -H "Authorization: Bearer $COMMUNITY_TOKEN" | python3 -m json.tool
echo ""

echo "=== テスト完了 ==="
