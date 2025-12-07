## CoCoIRU API - 使い方

このドキュメントはローカルで動作する CoCoIRU の FastAPI ベースの API の使い方をまとめたものです。

## 1. 概要
- ベース URL: `http://{HOST}:{PORT}/api/v1` （デフォルト起動例では `http://127.0.0.1:8000/api/v1`）
- 実装言語: Python + FastAPI
- DB: SQLite（開発/テスト環境）

各リソースは CRUD（Create / Read / Update / Delete）を提供します。主要なリソース:
- Special Notes: `/special_notes`
- Items: `/items`
- Shelter Info: `/shelter_info`
- Members: `/members`
- Request Content: `/request_content`
- Communities: `/communities`
- Shelter: `/shelter`
- Support Requests: `/support_requests`

## 2. 起動（開発用）
uvicorn を使って起動します。

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

起動後、OpenAPI ドキュメントは `http://127.0.0.1:8000/docs` で参照できます。

## 3. エンドポイント（主要な使い方 / サンプル）
以下は各リソースの基本操作（HTTP メソッド / パス / JSON 例）です。すべて `prefix` が `/api/v1` なので、ローカルでの完全なパスは例の先頭に `/api/v1` を付与してください。

-- Items (`/api/v1/items`)

- Create (POST)

```json
POST /api/v1/items/
{
  "item_name": "Water",
  "unit": "bottle",
  "category": "drink",
  "description": "500ml"
}
```

- Read list (GET)

GET /api/v1/items/

- Read one (GET)

GET /api/v1/items/{item_id}

- Update (PUT)

PUT /api/v1/items/{item_id}
{
  "item_name": "Updated Name",
  "unit": "pc",
  "category": "food",
  "description": "new"
}

- Delete (DELETE)

DELETE /api/v1/items/{item_id}

-- Special Notes (`/api/v1/special_notes`)

同様に POST/GET/PUT/DELETE をサポートします。POST は `notes_content_json` を受け取ります。

-- Members (`/api/v1/members`)

Members は `special_notes_id` に対する外部キーを持ちます。存在しない `special_notes_id` を指定して作成しようとすると DB の整合性違反（IntegrityError）が発生します。

例:

```json
POST /api/v1/members/
{
  "special_notes_id": 1
}
```

-- Request Content (`/api/v1/request_content`)

`items_id` (必須)、`number` (必須) を受け取り、品目と数量を表すレコードを作成します。

-- Communities (`/api/v1/communities`)

`member_id`（Members への外部キー）と `name`（作成時必須）などを保持します。

-- Shelter Info / Shelter (`/api/v1/shelter_info`, `/api/v1/shelter`)

避難所情報と避難所の CRUD を提供します。Shelter は `shelter_info` と `community_id` を外部キーに持ちます。

-- Support Requests (`/api/v1/support_requests`)

コミュニティと要請内容（RequestContent）を紐づけて支援要請を管理します。作成時は `community_id` と `request_content_id` が必須です。

## 4. バリデーション / エラーと取り扱い
- Pydantic による入力バリデーションにより、必須フィールドが欠けていると `422 Unprocessable Entity` を返します。
- DB の外部キー整合性違反 (IntegrityError) は `app/main.py` に定義された例外ハンドラで捕捉され、HTTP 409 (Conflict) として返却されます。
  - テスト環境では SQLite の外部キー制約を明示的に有効化しており、FK違反時に IntegrityError が発生することを前提にテストしています。

## 5. テストの実行方法
プロジェクトには pytest を使ったテスト群があります。テストは `tests/` 配下にあります。

```bash
python3 -m pytest -q
```

テスト環境では、`tests/conftest.py` がインメモリ SQLite を用いてテスト用 DB を作成し、各テストごとにトランザクションを張ってロールバックする方式を採用しています。外部キーの検証が効くよう PRAGMA による制約有効化も行っています。

## 6. 注意点とトラブルシュート
- SQLite はデフォルトで外部キー制約を有効にしないため、開発時/テスト時ともに明示的に有効化しています（`PRAGMA foreign_keys=ON`）。このため、ローカル実行とテスト実行で FK によるエラーが再現されます。
- テスト内で意図的に IntegrityError を発生させると、そのリクエストで使われたトランザクションがロールバックされ、同一セッションで続けて DB 操作を行う場合はセッションの状態をリセットする必要があります。テスト環境ではその点を考慮した実装になっています。

## 7. 開発上の改善ポイント（参考）
- SQLAlchemy 2.x 系に合わせた API への完全移行（`declarative_base` の import 位置など）。
- 認証・認可（現状は未実装）を追加してエンドポイントごとの権限制御を行う。
- 既存エンドポイントのレスポンス仕様を厳密にドキュメント（レスポンス例）化する。

---

もしこの README をさらに拡張してほしい場合（認証の追加手順、データシードスクリプト、各エンドポイントの完全な request/response サンプルなど）、要望を教えてください。
