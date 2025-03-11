import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

if __name__ == '__main__':
    msg = MIMEMultipart()
    msg['from'] = "management@messio.com"  # you cannot change this
    msg['to'] = "jeanpierre.cuvelliez@ulb.be"
    msg['subject'] = "Test email"
    msg.attach(MIMEText("<html><span style='color: green;'>Hello world</span></html>", 'html'))
    with open(Path.home() / 'smtp_password.txt') as f:
        password = f.read().strip()
        with smtplib.SMTP_SSL('akene.messio.com', 465) as server:
            server.set_debuglevel(1)
            server.login(msg['from'], password)
            server.sendmail(msg['from'], msg['to'], msg.as_string())
