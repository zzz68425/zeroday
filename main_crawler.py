# main_crawler.py
from zeroday_scraper import get_zd_ids_until
from process_vulnerability import process_vulnerability
import time, random, sys
from db import init_db, SessionLocal
from models import Incident
from logger_utils import logger, log_error, log_failed

init_db()
session = SessionLocal()
# 輸入目標 ZD-ID
first_row = session.query(Incident.id).order_by(Incident.sn.desc()).first()
if first_row is None:
    target_id = input("請輸入欲爬取編號（例如: ZD-2025-00245）：").strip()
    zd_ids = get_zd_ids_until(target_id)
else:
    target_id = first_row[0]
    zd_ids = get_zd_ids_until(target_id)
    zd_ids = zd_ids[1:]


print(f"\n共獲得 {len(zd_ids)} 筆 ZD ID")

for index, zdid in enumerate(zd_ids, start=1):
    for attempt in range(3):
        logger.info(f"第 {index}/{len(zd_ids)} 筆：處理 {zdid}（第 {attempt+1} 次嘗試）")
        result = process_vulnerability(zdid)

        if result in ("ok", "exists"):
            delay = random.uniform(2.5, 4.5)
            #print(f"等待 {delay:.1f} 秒後繼續...\n")
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
                sys.exit(1)

session.close()