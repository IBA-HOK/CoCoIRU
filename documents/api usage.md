## CoCoIRU API - 使い方

このドキュメントはローカルで動作する CoCoIRU の FastAPI ベースの API の使い方をまとめたものです。

## 1. 概要
- ベース URL: `http://{HOST}:{PORT}/api/v1` （デフォルト起動例では `http://127.0.0.1:8000/api/v1`）
- 実装言語: Python + FastAPI
- DB: SQLite（開発/テスト環境）
- 認証方式: OAuth2 (Bearer Token) + JWT

各リソースは CRUD（Create / Read / Update / Delete）を提供します。主要なリソース:
- Special Notes: `/special_notes`
- Items: `/items`
- Shelter Info: `/shelter_info`
- Members: `/members`
- Request Content: `/request_content`
- Communities: `/communities`
- Shelter: `/shelter`
- Support Requests: `/support_requests`
- Token: `/token`（認証）

## 2. 起動（開発用）
uvicorn を使って起動します。

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

起動後、OpenAPI ドキュメントは `http://127.0.0.1:8000/docs` で参照できます。

## 3. 認証（Authentication）

### 3.1 認証システムの概要
CoCoIRU API は JWT (JSON Web Token) を使用した Bearer Token 認証を採用しています。

- **認証方式**: OAuth2 Password Bearer
- **トークン形式**: JWT (HS256)
- **トークン有効期間**: デフォルト 10800秒 (3時間)
- **認証対象**: コミュニティ単位（community_id + password）

### 3.2 認証フロー

#### ステップ1: トークンの取得

コミュニティIDとパスワードを使ってアクセストークンを取得します。

```http
POST /api/v1/token
Content-Type: application/json

{
  "community_id": 1,
  "password": "your_password"
}
```

**レスポンス例**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 10800
}
```

**エラーレスポンス例**:
- 400 Bad Request: community_id または password が欠けている
- 401 Unauthorized: 認証情報が無効

#### ステップ2: トークンを使った API リクエスト

取得したトークンを `Authorization` ヘッダーに含めて API をリクエストします。

```http
GET /api/v1/items/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 3.3 認証が必要なエンドポイント

以下のエンドポイントは認証が必須です（Bearer Token が必要）:

- `/api/v1/items/*` - すべての Items エンドポイント
- `/api/v1/special_notes/*` - すべての Special Notes エンドポイント
- `/api/v1/shelter_info/*` - すべての Shelter Info エンドポイント
- `/api/v1/members/*` - すべての Members エンドポイント
- `/api/v1/request_content/*` - すべての Request Content エンドポイント
- `/api/v1/shelter/*` - すべての Shelter エンドポイント
- `/api/v1/support_requests/*` - すべての Support Requests エンドポイント
- `/api/v1/communities/*` - GET/PUT/DELETE エンドポイント（POST は認証不要）
- `/api/v1/gnss/*` - すべての GNSS エンドポイント

### 3.4 認証なしでアクセス可能なエンドポイント

- `POST /api/v1/token` - トークン取得（認証エンドポイント）
- `POST /api/v1/communities/` - 新規コミュニティ登録

### 3.5 環境変数による設定

認証システムは以下の環境変数で設定可能です:

```bash
# JWT秘密鍵（本番環境では必ず変更してください）
AUTH_SECRET_KEY=change-me

# JWT アルゴリズム
AUTH_ALGORITHM=HS256

# トークン有効期限（秒）
ACCESS_TOKEN_EXPIRE_SECONDS=10800

# 管理者ユーザー名（将来の拡張用）
ADMIN_USERNAME=admin

# 管理者パスワード（将来の拡張用）
ADMIN_PASSWORD=admin
```

### 3.6 コミュニティ登録とパスワード管理

新規コミュニティを作成する際、パスワードは自動的にハッシュ化されて `Credential` テーブルに保存されます。

```http
POST /api/v1/communities/
Content-Type: application/json

{
  "member_id": 1,
  "name": "Myコミュニティ",
  "password": "secure_password_here"
}
```

- パスワードは bcrypt でハッシュ化されて保存
- 平文パスワードは保存されません
- 認証時は bcrypt で検証

### 3.7 curl での使用例

```bash
# 1. トークン取得
TOKEN=$(curl -s -X POST "http://127.0.0.1:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"community_id": 1, "password": "your_password"}' \
  | jq -r '.access_token')

# 2. 認証付きでリソースを取得
curl -X GET "http://127.0.0.1:8000/api/v1/items/" \
  -H "Authorization: Bearer $TOKEN"

# 3. 認証付きでリソースを作成
curl -X POST "http://127.0.0.1:8000/api/v1/items/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"item_name": "Water", "unit": "bottle", "category": "drink", "description": "500ml"}'
```

### 3.8 認証エラーのハンドリング

認証に失敗した場合、以下のステータスコードが返されます:

- **401 Unauthorized**: トークンが無効、期限切れ、または欠けている
  ```json
  {
    "detail": "Invalid token"
  }
  ```

- **403 Forbidden**: トークンは有効だが、リソースへのアクセス権限がない（将来の拡張）

## 4. エンドポイント（主要な使い方 / サンプル）

以下は各リソースの基本操作（HTTP メソッド / パス / JSON 例）です。すべて `prefix` が `/api/v1` なので、ローカルでの完全なパスは例の先頭に `/api/v1` を付与してください。

**注意**: 以下のエンドポイント（Token と Communities の POST 以外）は認証が必要です。`Authorization: Bearer <token>` ヘッダーを含めてください。

### 4.1 Token (`/api/v1/token`) - 認証不要

- **トークン取得 (POST)**

```http
POST /api/v1/token
Content-Type: application/json

{
  "community_id": 1,
  "password": "your_password"
}
```

レスポンス:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 10800
}
```

### 4.2 Items (`/api/v1/items`) - 認証必須

- **Create (POST)**

```http
POST /api/v1/items/
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "item_name": "Water",
  "unit": "bottle",
  "category": "drink",
  "description": "500ml"
}
```

- **Read list (GET)**

```http
GET /api/v1/items/
Authorization: Bearer <your_token>
```

- **Read one (GET)**

```http
GET /api/v1/items/{item_id}
Authorization: Bearer <your_token>
```

- **Update (PUT)**

```http
PUT /api/v1/items/{item_id}
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "item_name": "Updated Name",
  "unit": "pc",
  "category": "food",
  "description": "new"
}
```

- **Delete (DELETE)**

```http
DELETE /api/v1/items/{item_id}
Authorization: Bearer <your_token>
```

### 4.3 Special Notes (`/api/v1/special_notes`) - 認証必須

同様に POST/GET/PUT/DELETE をサポートします。POST は `notes_content_json` を受け取ります。

```http
POST /api/v1/special_notes/
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "notes_content_json": {"note": "特記事項の内容"}
}
```

### 4.4 Members (`/api/v1/members`) - 認証必須

Members は `special_notes_id` に対する外部キーを持ちます。存在しない `special_notes_id` を指定して作成しようとすると DB の整合性違反（IntegrityError）が発生します。

例:

```http
POST /api/v1/members/
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "special_notes_id": 1
}
```

### 4.5 Request Content (`/api/v1/request_content`) - 認証必須

`items_id` (必須)、`number` (必須) を受け取り、品目と数量を表すレコードを作成します。

```http
POST /api/v1/request_content/
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "items_id": 1,
  "number": 10
}
```

### 4.6 Communities (`/api/v1/communities`)

`member_id`（Members への外部キー）と `name`（作成時必須）、`password`（作成時必須）などを保持します。

- **Create (POST)** - 認証不要

```http
POST /api/v1/communities/
Content-Type: application/json

{
  "member_id": 1,
  "name": "新規コミュニティ",
  "password": "secure_password"
}
```

- **Read list (GET)** - 認証必須

```http
GET /api/v1/communities/
Authorization: Bearer <your_token>
```

- **Read one (GET)** - 認証必須

```http
GET /api/v1/communities/{community_id}
Authorization: Bearer <your_token>
```

- **Update (PUT)** - 認証必須

```http
PUT /api/v1/communities/{community_id}
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "name": "更新されたコミュニティ名"
}
```

- **Delete (DELETE)** - 認証必須

```http
DELETE /api/v1/communities/{community_id}
Authorization: Bearer <your_token>
```

### 4.7 Shelter Info / Shelter (`/api/v1/shelter_info`, `/api/v1/shelter`) - 認証必須

避難所情報と避難所の CRUD を提供します。Shelter は `shelter_info` と `community_id` を外部キーに持ちます。

```http
POST /api/v1/shelter_info/
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "shelter_name": "避難所A",
  "address": "東京都XXX区YYY町1-2-3"
}
```

### 4.8 Support Requests (`/api/v1/support_requests`) - 認証必須

コミュニティと要請内容（RequestContent）を紐づけて支援要請を管理します。作成時は `community_id` と `request_content_id` が必須です。

```http
POST /api/v1/support_requests/
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "community_id": 1,
  "request_content_id": 1
}
```

## 5. バリデーション / エラーと取り扱い

- Pydantic による入力バリデーションにより、必須フィールドが欠けていると `422 Unprocessable Entity` を返します。
- DB の外部キー整合性違反 (IntegrityError) は `app/main.py` に定義された例外ハンドラで捕捉され、HTTP 409 (Conflict) として返却されます。
  - テスト環境では SQLite の外部キー制約を明示的に有効化しており、FK違反時に IntegrityError が発生することを前提にテストしています。
- 認証エラーは HTTP 401 (Unauthorized) として返却されます。
- トークンの有効期限切れも HTTP 401 (Unauthorized) として返却されます。

## 6. テストの実行方法

プロジェクトには pytest を使ったテスト群があります。テストは `tests/` 配下にあります。

```bash
python3 -m pytest -q
```

テスト環境では、`tests/conftest.py` がインメモリ SQLite を用いてテスト用 DB を作成し、各テストごとにトランザクションを張ってロールバックする方式を採用しています。外部キーの検証が効くよう PRAGMA による制約有効化も行っています。

## 7. セキュリティに関する注意点

### 7.1 本番環境での必須対応

- **AUTH_SECRET_KEY の変更**: デフォルトの `change-me` は必ず強力なランダム文字列に変更してください
  ```bash
  # 安全な秘密鍵の生成例
  openssl rand -hex 32
  ```

- **HTTPS の使用**: 本番環境では必ず HTTPS を使用してトークンの盗聴を防いでください
- **トークンの安全な保管**: クライアント側でトークンを localStorage や sessionStorage に保存する際は XSS 対策を徹底してください

### 7.2 パスワードポリシー

- パスワードは bcrypt でハッシュ化されて保存されます
- 最小文字数などのポリシーは現在実装されていません（将来の改善点）
- パスワードリセット機能は未実装です

### 7.3 レート制限

- 現在、レート制限は実装されていません
- 本番環境では API Gateway やリバースプロキシでレート制限を設定することを推奨します

## 8. 注意点とトラブルシュート

- SQLite はデフォルトで外部キー制約を有効にしないため、開発時/テスト時ともに明示的に有効化しています（`PRAGMA foreign_keys=ON`）。このため、ローカル実行とテスト実行で FK によるエラーが再現されます。
- テスト内で意図的に IntegrityError を発生させると、そのリクエストで使われたトランザクションがロールバックされ、同一セッションで続けて DB 操作を行う場合はセッションの状態をリセットする必要があります。テスト環境ではその点を考慮した実装になっています。
- トークンが期限切れの場合は、再度 `/api/v1/token` エンドポイントでトークンを取得してください。

## 9. 開発上の改善ポイント（参考）

- SQLAlchemy 2.x 系に合わせた API への完全移行（`declarative_base` の import 位置など）
- トークンのリフレッシュ機能の追加
- パスワードリセット機能の実装
- ロールベースのアクセス制御（RBAC）の実装
- レート制限の実装
- 監査ログの実装
- 既存エンドポイントのレスポンス仕様を厳密にドキュメント（レスポンス例）化する

---

もしこの README をさらに拡張してほしい場合（データシードスクリプト、各エンドポイントの完全な request/response サンプルなど）、要望を教えてください。
