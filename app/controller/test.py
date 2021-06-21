# from smtplib import SMTP                  # use this for standard SMTP protocol   (port 25, no encryption)
# old version
# from email.MIMEText import MIMEText
from email.mime.text import MIMEText
from smtplib import SMTP_SSL as SMTP  # this invokes the secure SMTP protocol (port 465, uses SSL)

SMTP_Host = 'smtp.gmail.com'
sender = 'khoaluan.tutor@gmail.com'
receivers = ['trongkhanhvip1@gmail.com']
username = "khoaluan.tutor@gmail.com"
password = "khoaluan2021"
# typical values for text_subtype are plain, html, xml
text_subtype = 'plain'
content = """\
Test SMTTP Python script
"""
subject = "Sent from vinasupport.com"


def test1():
    try:
        msg = MIMEText(content, text_subtype)
        msg['Subject'] = subject
        msg['From'] = sender  # some SMTP servers will do this automatically, not all
        conn = SMTP(SMTP_Host)
        conn.set_debuglevel(False)
        conn.login(username, password)
        try:
            conn.sendmail(sender, receivers, msg.as_string())
        finally:
            conn.quit()
    except Exception as error:
        print(error)
