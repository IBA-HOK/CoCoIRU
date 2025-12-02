#!/bin/bash

echo "=== ログインテスト ==="
curl -X POST http://127.0.0.1:8000/api/v1/login/login \
  -H "Content-Type: application/json" \
  -d '{"user_type":"gov","username":"gov_admin","password":"gov_admin_pass"}' \
  -c /tmp/test_cookies.txt \
  -s | python3 -m json.tool

echo ""
echo "=== Cookieの内容 ==="
cat /tmp/test_cookies.txt

echo ""
echo "=== /me エンドポイントテスト (Cookie使用) ==="
curl -X GET http://127.0.0.1:8000/api/v1/login/me \
  -b /tmp/test_cookies.txt \
  -s | python3 -m json.tool
