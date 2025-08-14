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
import pandas as pd
import os
import re

load_dotenv()
init_db()
session = SessionLocal()

# 處理弱點資料的函式，包含重試機制  
def process_with_retry(zdid, category_1_ids, index=None, total=None):
    max_retry = int(os.getenv("RETRY_COUNT", 3))
    logger.info(f"第 {index}/{total} 筆：處理 {zdid}")
    for attempt in range(max_retry):
        #logger.info(f"第 {index}/{total} 筆：處理 {zdid}（第 {attempt + 1} 次）")

        try:
            result = process_vulnerability(zdid, category_1_ids)
            return result
        except Exception as e:
            if attempt < max_retry - 1:
                #print("等待 10 秒後重試...")
                time.sleep(10)
            else:
                logger.error(f"{zdid} 失敗（第 {max_retry} 次）：{e}")
                log_failed(zdid)
                return "fail"

# 輸入目標 ZD-ID 並驗證格式
def input_valid_zdid():
    while True:
        zdid = input("請輸入欲爬取編號（例如: ZD-2025-00245）：").strip()
        if re.fullmatch(r"ZD-\d{4}-\d{5}", zdid):
            return zdid
        print("格式錯誤，請重新輸入。例如：ZD-2025-00245")

# 找出此次程式要處理的所有編號
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
stop_processing = False

# 處理每個 ZD-ID
for index, zdid in enumerate(zd_ids, start=1):
    if stop_processing:
        break
    result = process_with_retry(zdid, category_1_ids, index=index, total=len(zd_ids))
    if result == "fail":
        stop_processing = True
        break
    delay = random.uniform(2.5, 4.5)
    # time.sleep(delay)


# 從這次程式寫入的編號中找出第一筆作為索引找sn
first_zdid = zd_ids[0] if zd_ids else None
start_sn = None
if first_zdid:
    incident = session.query(Incident).filter_by(id=first_zdid).first()
    if incident:
        start_sn = incident.sn

# 查詢本成功寫入資料庫的incident數量
if start_sn:
    all = session.query(Incident).filter(Incident.sn >= start_sn).count()


# 查詢本次擷取範圍內的 category=1
df = query_category1_df(start_sn) if start_sn else pd.DataFrame()

# 寄送 Email
send_category1_report_from_df(
    df,
    all,
    sender_email=os.getenv("SENDER_EMAIL"),
    receiver_email=os.getenv("RECEIVER_EMAIL"),
    app_password=os.getenv("GOOGLE_APP_PASSWORD")
)

session.close()