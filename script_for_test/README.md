# CoCoIRU テストスクリプト

## スクリプト一覧

### 1. create_test_data.py（推奨）
開発・テスト用の初期データを自動作成するPythonスクリプト

#### 作成されるデータ
- Special Notes（特記事項）: 4件
- Members（メンバー）: 4件
- Communities（コミュニティ）: 4件
- Items（支援品目）: 10件
- Request Contents（要請内容）: 8件
- Support Requests（支援要請）: 8件
- Shelter Info（避難所情報）: 3件

#### 使用方法
```bash
# APIサーバーを起動
cd /home/hokuto/ドキュメント/github/CoCoIRU
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 &

# テストデータを作成
cd script_for_test
python3 create_test_data.py
```

#### 作成されるコミュニティアカウント
1. **北区避難所A** - ID: 1, パスワード: `community001`, メンバー数: 45人
2. **中央区避難所B** - ID: 2, パスワード: `community002`, メンバー数: 82人
3. **南区避難所C** - ID: 3, パスワード: `community003`, メンバー数: 63人
4. **西区避難所D** - ID: 4, パスワード: `community004`, メンバー数: 51人

#### Gov管理者アカウント
- ユーザー名: `gov_admin`
- パスワード: `gov_admin_pass`

### 2. testcom.js
コミュニティのID、リクエストコンテントのIDをbodyに指定しsupport_requestの配列を作成します。

#### 使用方法
```bash
# 依存パッケージをインストール（初回のみ）
cd /home/hokuto/ドキュメント/github/CoCoIRU
npm install

# APIサーバーを起動
uvicorn app.main:app --reload

# テストスクリプトを実行（別のターミナルで）
node script_for_test/testcom.js
```

初回実行時は自動的にシードコミュニティが作成され、その後テストコミュニティが生成されます。

## 必要な依存関係

### Python
```bash
pip3 install requests
```

### Node.js
```bash
npm install
```

## トラブルシューティング

### データベーススキーマエラーが出る場合
```bash
cd /home/hokuto/ドキュメント/github/CoCoIRU
rm -f database.db
python3 db/create_database.py
```

### エラー: "Gov管理者トークンが取得できませんでした"
- APIサーバーが起動しているか確認してください
- データベースが正しく初期化されているか確認してください

### エラー: "Address already in use"
- ポート8000が既に使用されています
  ```bash
  lsof -ti:8000 | xargs kill -9
  ```

### エラー: "インポート 'requests' を解決できませんでした"
- requestsライブラリをインストールしてください
  ```bash
  pip3 install requests
  ```
