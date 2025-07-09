# zeroday_scraper.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import time
from lib.logger_utils import logger
from lib.config import API_KEY
from lib.api_balance import balance

# ===== 共用設定 =====
KEY = API_KEY
TOKEN = f"Bearer {KEY}"
HEADERS = {
    "Authorization": TOKEN,
    "X-Return-Format": "html"
}

# ===== 工具函式 =====

# 查詢 TANet Whois 網域與機構
def query_tanet_whois(ip):
    try:
        res = requests.get(
            f"https://whois.tanet.edu.tw/showWhoisPublic.php?queryString={ip}",
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, "html.parser")
        td_tags = soup.find_all("td")

        institution = domain = None
        for i, td in enumerate(td_tags):
            if "用戶單位網段" in td.get_text(strip=True):
                if i + 2 < len(td_tags):
                    institution = td_tags[i + 2].get_text(strip=True)
                if i + 10 < len(td_tags):
                    domain_match = re.search(r"@([\w\.-]+)", td_tags[i + 10].get_text(strip=True))
                    if domain_match:
                        domain_str = domain_match.group(1)
                        if domain_str.endswith("edu.tw"):
                            domain = domain_str
                break
        return institution, domain
    except Exception as e:
        logger.warning(f"TANet Whois 查詢失敗：{e}")
        return None, None

# 從 Jina 抓取 ZD-ID，一直到指定目標
def get_zd_ids_until(target_zdid):
    zd_ids = []
    page = 1
    found = False
    while True:
        url = f"https://r.jina.ai/https://zeroday.hitcon.org/vulnerability/disclosed/page/{page}"
        res = fetch_with_retry(url, HEADERS, retries=3, delay=5)
        if res is None:
            break
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, "html.parser")

        page_found_any = False
        for li in soup.find_all("li", class_="code"):
            match = re.search(r"(ZD-\d{4}-\d{5})", li.get_text(strip=True))
            if match:
                zdid = match.group(1)
                page_found_any = True
                zd_ids.append(zdid)
                if zdid == target_zdid:
                    found = True
                    break
        if found:
            break
        if not page_found_any:
            break

        time.sleep(1.5)
        page += 1

    if not found:
        logger.error(f"找不到編號 ZD-ID：{target_zdid}，程式終止")
        return []

    return zd_ids[::-1]

# 抓 page：retry 機制
def fetch_with_retry(url, headers, retries=3, delay=5):
    for i in range(retries):
        try:
            res = requests.get(url, headers=headers, timeout=40)
            if res.status_code == 200:
                return res
            else:
                logger.warning(f"第 {i+1} 次嘗試，{url} 回應狀態碼：{res.status_code}")
        except Exception as e:
            logger.error(f"第 {i+1} 次嘗試失敗，錯誤：{e}")
        time.sleep(delay)
    logger.warning(f"token剩餘 : {balance}")
    return None
