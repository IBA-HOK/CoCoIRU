@echo off
cls

echo.
echo --- 依存関係をインストール・更新します (npm install) ---
npm install

REM npm installが成功したかチェック
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo !!! npm installに失敗しました。!!!
    pause
    exit /b
)

echo.
echo --- 開発サーバーを起動します (npm run dev) ---
npm run dev