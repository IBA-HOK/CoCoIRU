# ロールベースアクセス制御 (RBAC) 実装ガイド

## 概要

CoCoIRU APIに`gov`（政府管理者）ロールを追加し、APIごとにアクセス制御を実装しました。

## 実装内容

### 1. ユーザーロールの種類

- **community**: 一般のコミュニティユーザー
- **gov**: 政府管理者（全体の監視・管理権限を持つ）

### 2. データベーススキーマの変更

#### 新規テーブル: `GovUser`
```sql
CREATE TABLE GovUser (
    gov_user_id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    credential_id INTEGER NOT NULL UNIQUE,
    email TEXT,
    full_name TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TEXT,
    FOREIGN KEY (credential_id) REFERENCES Credential (credential_id)
);
```

#### 更新テーブル: `Credential`
- `Communities`と`GovUser`の両方から参照される共通の認証情報テーブル

### 3. 認証フロー

#### トークン取得エンドポイント: `POST /api/v1/token`

**コミュニティユーザーの場合:**
```json
{
  "user_type": "community",
  "community_id": 1,
  "password": "your_password"
}
```

**Gov管理者の場合:**
```json
{
  "user_type": "gov",
  "username": "gov_admin",
  "password": "gov_admin_pass"
}
```

**レスポンス:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 10800,
  "role": "gov"  // または "community"
}
```

#### JWTペイロード構造

```json
{
  "sub": "gov:gov_admin",  // または "community:1"
  "role": "gov",            // または "community"
  "exp": 1234567890
}
```

### 4. アクセス制御ポリシー

| エンドポイント | メソッド | アクセス権限 | 説明 |
|---------------|---------|------------|------|
| `/api/v1/token` | POST | 全員 | トークン取得 |
| `/api/v1/communities/` | POST | 全員 | コミュニティ新規登録 |
| `/api/v1/communities/` | GET | **gov専用** | 全コミュニティ一覧取得 |
| `/api/v1/communities/{id}` | GET/PUT/DELETE | 認証済み全員 | 個別コミュニティ操作 |
| `/api/v1/support_requests/` | GET | **gov専用** | 全支援要請一覧取得 |
| `/api/v1/support_requests/` | POST | 認証済み全員 | 支援要請作成 |
| `/api/v1/support_requests/{id}` | GET/PUT/DELETE | 認証済み全員 | 個別支援要請操作 |
| `/api/v1/items/*` | ALL | 認証済み全員 | 品目管理 |
| `/api/v1/special_notes/*` | ALL | 認証済み全員 | 特記事項管理 |
| `/api/v1/shelter_info/*` | ALL | 認証済み全員 | 避難所情報管理 |
| `/api/v1/members/*` | ALL | 認証済み全員 | メンバー管理 |
| `/api/v1/request_content/*` | ALL | 認証済み全員 | 要請内容管理 |
| `/api/v1/shelter/*` | ALL | 認証済み全員 | 避難所管理 |
| `/api/v1/gnss/*` | ALL | 認証済み全員 | GNSS管理 |

### 5. 実装されたセキュリティ関数

#### `app/core/security.py`

```python
# 既存の関数（拡張済み）
async def require_token(token: str = Depends(oauth2_scheme)) -> dict
    # トークン検証し、{"sub": "...", "role": "..."}を返す

# 新規関数
async def require_gov_role(token_data: dict = Depends(require_token)) -> dict
    # govロールを要求する
    
def verify_gov_credentials(username: str, password: str, db: Session) -> bool
    # gov管理者の認証
    
def create_access_token(data: dict, role: str, expires_delta: Optional[timedelta] = None) -> str
    # roleクレーム付きトークン生成
```

### 6. 初期gov管理者アカウント

データベース作成時に自動的に作成されます:

- **ユーザー名**: `gov_admin`
- **デフォルトパスワード**: `gov_admin_pass`
- **環境変数で変更可能**: `GOV_ADMIN_PASSWORD`

```bash
# 本番環境での設定例
export GOV_ADMIN_PASSWORD="your_secure_password"
python3 db/create_database.py
```

## 使用例

### 1. Gov管理者としてログイン

```bash
# トークン取得
curl -X POST "http://127.0.0.1:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{
    "user_type": "gov",
    "username": "gov_admin",
    "password": "gov_admin_pass"
  }'

# レスポンス
# {
#   "access_token": "eyJhbG...",
#   "token_type": "bearer",
#   "expires_in": 10800,
#   "role": "gov"
# }
```

### 2. Gov専用エンドポイントにアクセス

```bash
# 全コミュニティ一覧を取得（gov専用）
curl -X GET "http://127.0.0.1:8000/api/v1/communities/" \
  -H "Authorization: Bearer eyJhbG..."

# 全支援要請一覧を取得（gov専用）
curl -X GET "http://127.0.0.1:8000/api/v1/support_requests/" \
  -H "Authorization: Bearer eyJhbG..."
```

### 3. コミュニティユーザーとしてログイン

```bash
# 1. コミュニティを作成（認証不要）
curl -X POST "http://127.0.0.1:8000/api/v1/communities/" \
  -H "Content-Type: application/json" \
  -d '{
    "member_id": 1,
    "name": "テストコミュニティ",
    "password": "community_pass"
  }'

# 2. トークン取得
curl -X POST "http://127.0.0.1:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{
    "user_type": "community",
    "community_id": 1,
    "password": "community_pass"
  }'

# 3. 個別リソースにアクセス（認証済み全員OK）
curl -X GET "http://127.0.0.1:8000/api/v1/communities/1" \
  -H "Authorization: Bearer <community_token>"

# 4. Gov専用エンドポイントにアクセス（403エラー）
curl -X GET "http://127.0.0.1:8000/api/v1/communities/" \
  -H "Authorization: Bearer <community_token>"
# => {"detail": "Insufficient permissions. Gov role required."}
```

## エラーレスポンス

### 401 Unauthorized
```json
{
  "detail": "Invalid token"
}
```
トークンが無効、期限切れ、または欠けている場合。

### 403 Forbidden
```json
{
  "detail": "Insufficient permissions. Gov role required."
}
```
govロールが必要なエンドポイントにcommunityユーザーがアクセスした場合。

## セキュリティ上の注意点

1. **本番環境では必ずパスワードを変更**
   ```bash
   export GOV_ADMIN_PASSWORD="強力なランダムパスワード"
   ```

2. **HTTPS の使用**
   本番環境では必ずHTTPSを使用してトークンの盗聴を防ぐ

3. **トークンの有効期限**
   デフォルト3時間（10800秒）、`ACCESS_TOKEN_EXPIRE_SECONDS`で調整可能

4. **パスワードのハッシュ化**
   bcryptを使用して全パスワードをハッシュ化して保存

## 今後の拡張案

1. **追加のgovユーザー作成API**
   - `POST /api/v1/gov/users/` (gov専用)
   
2. **きめ細かいパーミッション管理**
   - 読み取り専用gov、編集可能govなど
   
3. **監査ログ**
   - gov操作の全履歴記録
   
4. **トークンリフレッシュ機能**
   - 長時間セッションのサポート

5. **リソースの所有権チェック**
   - コミュニティは自分のリソースのみ編集可能
