# Description
此程式為根據使用者需求自動或手動擷取zeroday網站上的資料並存入資料庫
## Requirement
python >= 3.10
## package
beautifulsoup4
pandas
python-dotenv
requests
sqlacodegen
## .env Setting
APP_PASSWORD
取得方法如:
https://steam.oxxostudio.tw/category/python/example/gmail.html
## Usage
1.建一個.env並設置APP_PASSWORD
2.在config.py中輸入jina金鑰、寄件者、收件者,jina金鑰在 https://jina.ai/zh-TW/ 取得
3.在main_crawler.py執行程式
4.可以在logs資料夾查看擷取結果