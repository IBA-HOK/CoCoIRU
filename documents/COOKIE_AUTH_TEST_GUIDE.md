# Cookie認証テスト手順書

## 概要
HTTPOnly Cookie + トークンブラックリスト機能のブラウザ動作確認手順です。

---

## 🚀 起動手順

### 1. バックエンドAPIサーバーの起動

```bash
cd /home/hokuto/ドキュメント/github/CoCoIRU
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**確認:**
- ブラウザで http://127.0.0.1:8000/health にアクセス
- `{"status":"ok","message":"Welcome to CoCoIRU API"}` が表示されればOK

### 2. Svelte開発サーバーの起動

```bash
cd ./Svelte
npm run dev
```

**確認:**
- ブラウザで http://localhost:5173 にアクセス
- Svelteアプリが表示されればOK

### 3. テストデータの作成（初回のみ）

```bash
python3 script_for_test/create_test_data.py
```

**確認:**
- "✓ テストデータ作成完了!" が表示されればOK

**注意（初回セットアップ）**:
- もしログインで `Invalid credentials` や `Missing bearer token` が出る場合は、初期 `gov_admin` アカウントが存在しない可能性があります。リポジトリに付属の DB 初期化スクリプトで作成できます:

```bash
python3 db/create_database.py
```

このコマンドは `database.db` のテーブルを作成し、デフォルトの `gov_admin` (パスワード: `gov_admin_pass`) を作成します。CI や本番では環境変数 `GOV_ADMIN_PASSWORD` を使ってパスワードを設定してください。

---

## 🧪 Cookie認証テスト手順

### テストページへのアクセス
ブラウザで以下のURLを開く:
```
http://localhost:5173/login_test
```

### ステップ1: Gov管理者でログイン

1. **ユーザータイプ**: 「Gov管理者」を選択
2. **ユーザー名**: `gov_admin`（デフォルト入力済み）
3. **パスワード**: `gov_admin_pass`（デフォルト入力済み）
4. **「ログイン」ボタン**をクリック

**期待される結果:**
- ✅ ログイン成功バッジが表示される
- 📝 ログインレスポンスが表示される
  ```json
  {
    "access_token": "eyJhbGci...",
    "token_type": "bearer",
    "expires_in": 10800,
    "role": "gov"
  }
  ```
- 👤 ユーザー情報が自動取得される
  ```json
  {
    "sub": "gov:gov_admin",
    "role": "gov"
  }
  ```

### ステップ2: ブラウザDevToolsでCookie確認

1. **F12キー**を押して開発者ツールを開く
2. **Application（またはStorage）タブ**を選択
3. **Cookies** → **http://localhost:5173** を展開
4. **`access_token`** Cookieを確認

**期待される確認項目:**
- ✅ `HttpOnly`: チェック済み（JavaScriptからアクセス不可）
- ✅ `SameSite`: Lax
- ✅ `Path`: /
- ✅ `Expires`: 3時間後（10800秒）

**補足（よくある失敗）**:
- ログインで `Set-Cookie` ヘッダが返っていても、ブラウザ側が Cookie を保存または送信しないことがあります。Network タブでログインレスポンスに `Set-Cookie` が含まれているか、属性（Domain/Path/SameSite/Secure）を確認してください。

### ステップ3: Cookie自動送信の確認

1. **「🔄 ユーザー情報を再取得」ボタン**をクリック

**期待される結果:**
- ✅ 追加の認証情報入力なしでユーザー情報が取得される
- DevToolsの**Networkタブ**で `/api/v1/login/me` リクエストを確認
- **Request Headers**に `Cookie: access_token=eyJhbGci...` が含まれる

**重要:** フロントエンド側の `fetch()` を使う場合、クロスオリジンのやり取りではブラウザはデフォルトで Cookie を送信しません。Cookie を自動送信するには `credentials: 'include'` を必ず付与してください:

```javascript
// 例: ユーザー情報取得
fetch('http://localhost:8000/api/v1/login/me', {
   method: 'GET',
   credentials: 'include'
});
```

`credentials: 'include'` がないとサーバー側で `Missing bearer token`（401）が返されます。

### ステップ4: ロールベースアクセス制御の確認

1. **「🔒 Gov専用エンドポイントテスト」ボタン**をクリック

**期待される結果:**
- ✅ アラートが表示される: "✅ Gov専用エンドポイントアクセス成功！"
- コミュニティ数が表示される（例: `コミュニティ数: 4`）
- DevToolsで `/api/v1/communities/` リクエストが200 OKを返す

**補足:** このエンドポイントは `require_gov_role` で保護されており、Gov管理者のみアクセス可能です。

### ステップ5: ログアウトとブラックリスト登録

1. **「🚪 ログアウト」ボタン**をクリック

**期待される結果:**
- ✅ ログイン画面に戻る
- DevToolsの**Applicationタブ**で `access_token` Cookieが削除される
- サーバー側でトークンがブラックリストに登録される

### ステップ6: ブラックリスト機能の確認

#### 方法A: ブラウザバックでの再アクセステスト

1. ブラウザの**戻るボタン**を押す
2. ログイン後の画面が一瞬表示される（ブラウザキャッシュ）
3. 「🔄 ユーザー情報を再取得」をクリック

**期待される結果:**
- ❌ エラーが表示される: "Token has been revoked"
- ステータスコード: 401 Unauthorized

#### 方法B: 手動でのトークン再利用テスト

1. ログアウト前にDevToolsで `access_token` の値をコピー
2. ログアウト
3. DevToolsの**Consoleタブ**で以下を実行:
   ```javascript
   fetch('http://127.0.0.1:8000/api/v1/login/me', {
     headers: {
       'Authorization': 'Bearer <コピーしたトークン>'
     }
   }).then(r => r.json()).then(console.log)
   ```

**期待される結果:**
- ❌ エラーレスポンス: `{"detail":"Token has been revoked"}`
- ブラックリストされたトークンは再利用不可

---

## 🧪 追加テスト: コミュニティユーザーでのアクセス制限

### ステップ1: コミュニティユーザーでログイン

1. ログインページで**ユーザータイプ**: 「コミュニティ」を選択
2. **コミュニティID**: `5`
3. **パスワード**: `community001`
4. 「ログイン」をクリック

**期待される結果:**
- ✅ ログイン成功
- 👤 ユーザー情報: `{"sub": "community:5", "role": "community"}`

### ステップ2: Gov専用エンドポイントアクセステスト

1. **「🔒 Gov専用エンドポイントテスト」ボタン**が**表示されない**ことを確認
   - このボタンは `role === 'gov'` の場合のみ表示される

2. DevToolsの**Consoleタブ**で手動アクセス:
   ```javascript
   fetch('http://127.0.0.1:8000/api/v1/communities/', {
     credentials: 'include'
   }).then(r => r.json()).then(console.log)
   ```

**期待される結果:**
- ❌ エラーレスポンス: `{"detail":"Insufficient permissions"}`
- ステータスコード: 403 Forbidden
- コミュニティユーザーはGov専用エンドポイントにアクセス不可

---

## 📊 テスト結果チェックリスト

### 基本機能
- [ ] Gov管理者でログイン成功
- [ ] コミュニティユーザーでログイン成功
- [ ] HTTPOnly Cookieが正しく設定される
- [ ] Cookie自動送信でユーザー情報取得成功

### セキュリティ機能
- [ ] ログアウト後にCookieが削除される
- [ ] ブラックリストされたトークンは再利用不可（401エラー）
- [ ] JavaScriptから `document.cookie` でトークンを読み取れない（HTTPOnly）
- [ ] Gov専用エンドポイントへのアクセス制御が機能

### ロールベースアクセス制御（RBAC）
- [ ] Gov管理者は全コミュニティ一覧を取得可能
- [ ] コミュニティユーザーはGov専用エンドポイントにアクセス不可（403）
- [ ] 各ロールのユーザー情報に正しい `role` フィールドが含まれる

---

## 🐛 トラブルシューティング

### Cookieが設定されない

**症状:** ログイン後にDevToolsでCookieが確認できない

**原因と対処:**
1. **CORS設定の確認**
   - `app/main.py` で `allow_credentials=True` が設定されているか確認
   - `allow_origins` に `http://localhost:5173` が含まれているか確認

2. **fetch呼び出しの確認**
   - `credentials: 'include'` が設定されているか確認

3. **ドメインの不一致**
   - APIとフロントエンドのドメインが異なる場合、`SameSite=None; Secure` が必要

**さらに詳しいチェックリスト（Cookieが送信されない場合）**
1. ログインのレスポンスに `Set-Cookie` があるか（Network → Response Headers）
2. `Set-Cookie` の `Domain` が期待するホストを指しているか（`localhost` と `127.0.0.1` は別扱い）
3. クライアント側の `fetch` に `credentials: 'include'` があるか（必須）
4. サーバーの CORS 設定で `allow_credentials=True` が有効か（`app/main.py` 参照）
5. ブラウザの DevTools → Application (Storage) で Cookie が保存されているか

**注意:** `SameSite=None` を使用する場合、ブラウザは `Secure=True` が付いていない Cookie を拒否するため HTTPS が必須になります。開発環境では `SameSite=Lax` と `secure=False` のまま、`credentials: 'include'` とホスト一致で運用するのが現実的です。

### 401 Unauthorized エラー（ログアウト前）

**症状:** ログイン後すぐに401エラーが発生

**原因と対処:**
1. **トークンの有効期限切れ**
   - デフォルトは3時間（10800秒）
   - `app/core/config.py` の `access_token_expire_seconds` を確認

2. **Cookie取得ロジックの確認**
   - `app/core/security.py` の `require_token` 関数を確認
   - `request.cookies.get("access_token")` が正しく動作しているか確認

**ホスト不一致 (localhost vs 127.0.0.1)**
- 開発用に API を `127.0.0.1:8000` で立てつつフロントを `localhost:5173` で動かすと、Cookie の発行ホストとアクセス元が一致しないため Cookie が送られないことがあります。推奨対策は次のどちらかです:

- フロントから API を同じホスト/ポートに合わせる（例: フロントからも `http://127.0.0.1:8000` を使う）
- Vite 開発サーバーの proxy を使って同一オリジン化する（推奨）

Vite proxy の例（`Svelte/vite.config.ts` または `vite.config.js` に追加）:

```ts
// vite.config.ts (一例)
import { defineConfig } from 'vite'

export default defineConfig({
   server: {
      proxy: {
         '/api': {
            target: 'http://127.0.0.1:8000',
            changeOrigin: true,
            secure: false,
         }
      }
   }
});
```

プロキシを使うと、フロントは `http://localhost:5173/api/...` にリクエストし、ブラウザから見て同一オリジンとなるため Cookie の送受信問題が解消します。

### ログアウト後もアクセスできてしまう

**症状:** ログアウト後にユーザー情報が取得できる

**原因と対処:**
1. **ブラックリスト機能の確認**
   - `db/crud.py` の `is_token_blacklisted` が正しく実装されているか確認
   - `TokenBlacklist` テーブルが存在するか確認
     ```bash
     sqlite3 database.db "SELECT * FROM TokenBlacklist;"
     ```

2. **データベース再作成**
   ```bash
   rm database.db
   python3 db/create_database.py
   python3 script_for_test/create_test_data.py
   ```

---

## 📝 実装詳細

### Cookie設定（login.py）
```python
response.set_cookie(
    key="access_token",
    value=access_token,
    httponly=True,  # JavaScriptからアクセス不可
    max_age=settings.access_token_expire_seconds,
    secure=False,  # 開発環境用。本番ではTrue
    samesite="lax"
)
```

### Cookie取得（security.py）
```python
async def require_token(
    request: Request,
    authorization: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> dict:
    # Cookie優先でトークン取得
    access_token = request.cookies.get("access_token")
    token = access_token or authorization
    
    # ブラックリストチェック
    if crud.is_token_blacklisted(db, token):
        raise HTTPException(401, "Token has been revoked")
    
    # JWT検証
    payload = decode_access_token(token)
    return {"sub": payload["sub"], "role": payload["role"], "token": token}
```

### ブラックリスト登録（login.py）
```python
@router.post("/logout")
def logout(
    response: Response,
    token_data: dict = Depends(require_token),
    db: Session = Depends(get_db)
):
    token = token_data.get("token")
    payload = decode_access_token(token)
    expires_at = datetime.fromtimestamp(payload.get("exp")).isoformat()
    
    # ブラックリストに追加
    crud.add_token_to_blacklist(db, token, expires_at)
    
    # Cookieを削除
    response.delete_cookie(key="access_token")
    
    return {"message": "Successfully logged out"}
```

---

## ✅ テスト完了

すべてのテストが成功すれば、Cookie認証とトークンブラックリスト機能が正しく動作しています！

**次のステップ:**
- 本番環境用にCookie設定を `secure=True` に変更
- トークンの有効期限を適切に調整
- 定期的なブラックリストクリーンアップ処理の実装
- リフレッシュトークン機能の追加（オプション）
