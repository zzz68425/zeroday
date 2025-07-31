# 寄信設定
import smtplib
from email.message import EmailMessage
import io
import pandas as pd


def send_category1_report_from_df(df: pd.DataFrame, sender_email: str, receiver_email: str, app_password: str):
    if df.empty:
        print("DataFrame 為空，未寄送 email")
        return

    msg = EmailMessage()
    msg["Subject"] = f"本次共擷取到 {len(df)} 筆 category=1 漏洞清單"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content("請見附件的 CSV 漏洞報告")

    # 轉換成 CSV bytes 附件
    buffer = io.StringIO() #建立文字緩衝區
    df.to_csv(buffer, index=False, encoding="utf-8-sig")
    csv_bytes = buffer.getvalue().encode("utf-8-sig")

    msg.add_attachment(
        csv_bytes,
        maintype="application",
        subtype="octet-stream",
        filename="category1_report.csv"
    )

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)
        print("Email 寄送成功")
    except Exception as e:
        print("Email 寄送失敗：", e)