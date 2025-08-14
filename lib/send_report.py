# 寄信設定
import smtplib
from email.message import EmailMessage
import io
import pandas as pd
from datetime import datetime


def send_category1_report_from_df(df: pd.DataFrame, total: int, sender_email: str, receiver_email: str, app_password: str):
    
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    now_date = datetime.now().strftime("%Y%m%d")
    
    msg = EmailMessage()
    msg["Subject"] = f"ZeroDay 擷取報告"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content(f"本次於 {now_str} 擷取 {total} 筆網站 ， 其中有 {len(df)} 筆是教育網站。")

    if not df.empty:
        # 轉換成 CSV bytes 附件
        buffer = io.StringIO() #建立文字緩衝區
        df.to_csv(buffer, index=False, encoding="utf-8-sig")
        csv_bytes = buffer.getvalue().encode("utf-8-sig")

        msg.add_attachment(
            csv_bytes,
            maintype="application",
            subtype="octet-stream",
            filename=f"result_{now_date}.csv"
        )

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)
        print("Email 寄送成功")
    except Exception as e:
        print("Email 寄送失敗：", e)