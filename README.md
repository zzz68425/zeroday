# Description

此程式為根據使用者需求自動或手動擷取 zeroday 網站上的資料並存入資料庫

## Requirement

python >= 3.10

## package

beautifulsoup4
pandas
python-dotenv
requests
sqlacodegen

## .env Setting

```
JINA_API_KEY
GOOGLE_APP_PASSWORD
SENDER_EMAIL
RECIPIENT_EMAIL
```

## Usage

1. 安裝 Git 版本控制軟體
2. 安裝 uv 套件管理軟體
3. 複製 GitHub 儲存庫
4. 取得 Google 應用程式密碼 取得方法:
   https://steam.oxxostudio.tw/category/python/example/gmail.html
5. 取得 Jina API Key 取得方法:開無痕視窗查https://jina.ai/zh-TW/
6. 複製 .env.example 為 .env
7. 設定 `GOOGLE_APP_PASSWORD` 環境變數（於第 4 步取得）
8. 設定 `JINA_API_KEY` 環境變數（於第 5 步取得）
9. 設定 `SENDER_EMAIL` 環境變數（教育網站彙報的寄件者）
10. 設定 `RECIPIENT_EMAIL` 環境變數（教育網站彙報的收件者）
