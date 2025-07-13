#就是log
import os
import logging
from datetime import datetime
from lib.api_balance import balance

# 建立 logs 資料夾
base_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(base_dir,"logs")
os.makedirs(log_dir, exist_ok=True)

now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = os.path.join(log_dir, f"crawler_{now_str}.log")

logger = logging.getLogger("crawler_logger")
logger.setLevel(logging.INFO)

#避免重複加 handler
if not logger.handlers:
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")

    # File handler
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Optional: Console handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

# 錯誤紀錄：記錄失敗次數與 log
def log_error(zdid, attempt, msg=""):
    logger.error(f"ZD-ID: {zdid} - 第 {attempt} 次失敗{msg}")

# 記錄永久失敗 ID
def log_failed(zdid):
    logger.warning(f"ZD-ID: {zdid} - 擷取失敗 - token剩餘 : {balance}")