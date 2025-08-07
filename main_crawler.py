# 主程式
from lib.zeroday_scraper import get_zd_ids_until
from lib.process_vulnerability import process_vulnerability
import time, random, sys
from lib.db.db import init_db, SessionLocal
from lib.db.models import Incident
from lib.logger_utils import logger, log_error, log_failed
from lib.send_report import send_category1_report_from_df
from lib.query import query_category1_df
from dotenv import load_dotenv
import os
import re

load_dotenv()

init_db()
session = SessionLocal()


# 輸入目標 ZD-ID 並驗證格式
def input_valid_zdid():
    while True:
        zdid = input("請輸入欲爬取編號（例如: ZD-2025-00245）：").strip()
        if re.fullmatch(r"ZD-\d{4}-\d{5}", zdid):
            return zdid
        print("格式錯誤，請重新輸入。例如：ZD-2025-00245")


# 輸入目標 ZD-ID
first_row = session.query(Incident.id).order_by(Incident.sn.desc()).first()
if first_row is None:
    target_id = input_valid_zdid()
    zd_ids = get_zd_ids_until(target_id)
else:
    target_id = first_row[0]
    zd_ids = get_zd_ids_until(target_id)
    zd_ids = zd_ids[1:]


print(f"\n共獲得 {len(zd_ids)} 筆 ZD ID")

category_1_ids = []
stop_processing = False  # 用來標記是否停止抓取後續資料

for index, zdid in enumerate(zd_ids, start=1):
    if stop_processing:
        break  # 如果已經標記需要停止處理，跳出外層循環
    
    for attempt in range(3):
        logger.info(f"第 {index}/{len(zd_ids)} 筆：處理 {zdid}（第 {attempt+1} 次嘗試）")
        result = process_vulnerability(zdid, category_1_ids)

        if result in ("ok", "exists"):
            delay = random.uniform(2.5, 4.5)
            #time.sleep(delay)
            break
        else:
            log_error(zdid, attempt+1)
            if attempt <= 1:
                print("等待 10 秒後重試...\n")
                time.sleep(10)
            else:
                logger.info(f"{zdid} 三次皆擷取失敗，終止程式\n")
                log_failed(zdid)
                stop_processing = True
                break

# mail通知使用者
df = query_category1_df()
send_category1_report_from_df(
    df,
    len(zd_ids),
    sender_email=os.getenv("SENDER_EMAIL"),
    receiver_email=os.getenv("RECEIVER_EMAIL"),
    app_password=os.getenv("GOOGLE_APP_PASSWORD")# 要去google設定
)
session.close()