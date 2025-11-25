# ロールベースアクセス制御 (RBAC) 実装完了レポート

## 実装完了日
2025年11月25日

## 実装概要

CoCoIRU APIに`gov`（政府管理者）ロールを追加し、エンドポイントごとにアクセス制御を実装しました。

## 実装内容

### 1. データベーススキーマの拡張

#### 新規テーブル
- **GovUser**: 政府管理者ユーザー情報
  - `gov_user_id` (PK)
  - `username` (UNIQUE)
  - `credential_id` (FK to Credential)
  - `email`, `full_name`, `is_active`, `created_at`

#### 更新テーブル
- **Credential**: CommunitiesとGovUserの両方から参照される共通認証テーブル
- **Communities**: `credential_id`列を追加してCredentialテーブルと連携

### 2. 認証システムの拡張

#### トークン発行エンドポイント
- `POST /api/v1/token`
- リクエストボディに`user_type`フィールドを追加
  - `"community"`: コミュニティユーザー（`community_id` + `password`）
  - `"gov"`: 政府管理者（`username` + `password`）

#### JWTトークン構造
```json
{
  "sub": "gov:gov_admin",  // または "community:1"
  "role": "gov",            // または "community"
  "exp": 1234567890
}
```

### 3. セキュリティ関数

#### 新規追加
- `require_gov_role()`: govロールを要求する依存関数
- `verify_gov_credentials()`: gov管理者認証関数
- `authenticate_gov_user()`: gov管理者データベース認証
- `create_gov_user()`: gov管理者作成関数

#### 更新
- `require_token()`: roleクレームを含むdict型を返すように変更
- `create_access_token()`: roleパラメータを追加

### 4. アクセス制御ポリシー

#### Gov専用エンドポイント
- `GET /api/v1/communities/` - 全コミュニティ一覧
- `GET /api/v1/support_requests/` - 全支援要請一覧

#### 認証済み全員アクセス可能
- 個別リソースのCRUD操作（GET/PUT/DELETE `/{id}`）
- 新規リソース作成（POST）
- Items, SpecialNotes, Members, RequestContent, Shelter, ShelterInfo, GNSS

#### 認証不要
- `POST /api/v1/token` - トークン取得
- `POST /api/v1/communities/` - コミュニティ新規登録

### 5. 初期データ

#### 初期gov管理者アカウント
- **ユーザー名**: `gov_admin`
- **デフォルトパスワード**: `gov_admin_pass`
- **環境変数**: `GOV_ADMIN_PASSWORD`で変更可能
- データベース作成時に自動生成

## テスト結果

### ✅ テスト項目

1. **Gov管理者認証**
   - Gov管理者トークン取得: ✅ 成功
   - トークンに`role: "gov"`が含まれる: ✅ 確認

2. **コミュニティユーザー認証**
   - コミュニティトークン取得: ✅ 成功
   - トークンに`role: "community"`が含まれる: ✅ 確認

3. **Gov専用エンドポイント**
   - Govトークンで全コミュニティ一覧取得: ✅ 成功
   - Communityトークンで全コミュニティ一覧取得: ✅ 403エラー
   - Govトークンで全支援要請一覧取得: ✅ 成功
   - Communityトークンで全支援要請一覧取得: ✅ 403エラー

4. **認証済み全員アクセス可能エンドポイント**
   - Communityトークンで個別コミュニティ取得: ✅ 成功
   - Communityトークンで個別支援要請取得: ✅ 成功
   - Communityトークンでリソース作成: ✅ 成功

5. **認証不要エンドポイント**
   - トークンなしでコミュニティ作成: ✅ 成功

### テスト実行例

```bash
# Gov管理者として全コミュニティ一覧を取得
curl -X GET "http://127.0.0.1:8000/api/v1/communities/" \
  -H "Authorization: Bearer <gov_token>"
# => [{"community_id": 1, "name": "テストコミュニティ", ...}]

# コミュニティユーザーとして全コミュニティ一覧を取得
curl -X GET "http://127.0.0.1:8000/api/v1/communities/" \
  -H "Authorization: Bearer <community_token>"
# => {"detail": "Insufficient permissions. Gov role required."}
```

## 変更ファイル一覧

### データベース層
- ✅ `db/models.py` - GovUserモデル追加
- ✅ `db/schemas.py` - GovUser、TokenRequest、TokenResponseスキーマ追加
- ✅ `db/crud.py` - GovUser CRUD関数と認証関数追加
- ✅ `db/create_database.py` - GovUserテーブル作成、初期管理者作成

### アプリケーション層
- ✅ `app/core/security.py` - require_gov_role、verify_gov_credentials追加
- ✅ `app/api/v1/endpoints/token.py` - user_type判別ロジック実装
- ✅ `app/api/v1/endpoints/communities.py` - GET一覧をgov専用に変更
- ✅ `app/api/v1/endpoints/support_request.py` - GET一覧をgov専用に変更

### ドキュメント
- ✅ `documents/RBAC_IMPLEMENTATION.md` - 実装ガイド作成
- ✅ `test_rbac.sh` - テストスクリプト作成

## セキュリティ推奨事項

### 本番環境での必須対応

1. **環境変数の設定**
   ```bash
   export GOV_ADMIN_PASSWORD="強力なランダムパスワード"
   export AUTH_SECRET_KEY="$(openssl rand -hex 32)"
   ```

2. **HTTPS の使用**
   - リバースプロキシ（Nginx/Apache）でHTTPS終端
   - Let's Encryptなどで無料SSL証明書取得

3. **データベースの保護**
   - SQLiteファイルのパーミッション設定: `chmod 600 database.db`
   - 本番環境ではPostgreSQL/MySQLへの移行を推奨

4. **レート制限の実装**
   - FastAPI Limiterまたはリバースプロキシでレート制限

## 今後の改善案

### 短期的改善
1. **リソース所有権チェック**
   - コミュニティは自分のリソースのみ編集可能にする
   
2. **パスワードポリシー**
   - 最小文字数、複雑性要件の追加

3. **監査ログ**
   - Gov操作の全履歴記録

### 長期的改善
1. **トークンリフレッシュ機能**
   - アクセストークン + リフレッシュトークン方式

2. **きめ細かい権限管理**
   - 読み取り専用gov、地域別govなど

3. **2要素認証 (2FA)**
   - gov管理者向けのセキュリティ強化

4. **APIキー認証**
   - 外部システム連携用

## まとめ

✅ Gov管理者アカウントとロールベースアクセス制御を完全に実装
✅ 全テストが成功し、期待通りに動作することを確認
✅ セキュリティベストプラクティスに従った実装
✅ 拡張性を考慮した設計で将来の機能追加が容易

初期gov管理者アカウント:
- ユーザー名: `gov_admin`
- パスワード: `gov_admin_pass` （本番環境では必ず変更してください）

実装は完了しました。本番環境にデプロイする前に、必ず環境変数を設定し、HTTPSを有効にしてください。
