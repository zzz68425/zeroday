# 寄信設定

import smtplib
from email.message import EmailMessage

def send_category1_report(ids: list[str], sender_email: str, receiver_email: str, app_password: str):
    if not ids:
        return

    msg = EmailMessage()
    msg["Subject"] = f"本次共擷取到{len(ids)}筆 category=1 漏洞清單"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    body = "以下是本次執行擷取到的 category=1 漏洞頁面編號：\n\n"
    body += "\n".join(ids)

    msg.set_content(body)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)
        print("Email 寄送成功")
    except Exception as e:
        print("Email 寄送失敗：", e)