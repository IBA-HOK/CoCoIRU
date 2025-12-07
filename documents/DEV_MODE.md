# 開発モード（認証バイパス）ガイド

## 概要
開発中のテストを容易にするため、環境変数 `DEV_MODE=true` を設定することで、すべてのAPI認証をバイパスできます。

## 使い方

### PowerShell（Windows）

```powershell
$env:DEV_MODE="true"; uvicorn app.main:app --reload --port 8000
```

または、個別に設定：

```powershell
$env:DEV_MODE="true"
uvicorn app.main:app --reload --port 8000
```

### Bash（Linux/Mac）

```bash
DEV_MODE=true uvicorn app.main:app --reload --port 8000
```

## 動作

開発モードが有効な場合：
- すべての認証チェックがスキップされます
- すべてのリクエストが `admin` ロールとして扱われます
- トークンの検証、Cookie認証、ブラックリストチェックが無効になります

ログには以下のメッセージが表示されます：
```
DEBUG: DEV_MODE is enabled, bypassing authentication
```

## 注意事項

⚠️ **本番環境では絶対に使用しないでください**

- この機能は開発・テスト専用です
- セキュリティが完全に無効化されます
- 本番環境やステージング環境では `DEV_MODE` を設定しないでください

## 通常モードへの戻し方

環境変数を削除または `false` に設定：

### PowerShell
```powershell
$env:DEV_MODE="false"
# または
Remove-Item Env:\DEV_MODE
```

### Bash
```bash
unset DEV_MODE
# または
DEV_MODE=false uvicorn app.main:app --reload --port 8000
```

## Svelte の package.json に追加する場合

`Svelte/package.json` の `scripts` セクションに追加：

```json
{
  "scripts": {
    "api": "uvicorn app.main:app --reload --port 8000",
    "api:dev": "cross-env DEV_MODE=true uvicorn app.main:app --reload --port 8000"
  }
}
```

※ `cross-env` パッケージが必要です：
```bash
npm install --save-dev cross-env
```

使用方法：
```bash
npm run api:dev
```
