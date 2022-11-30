from email.message import EmailMessage
import ssl
import smtplib

subject = "This is a test"
body = "This is a test email"

msg = EmailMessage()
msg['From'] = 'dtechnologyg215@gmail.com'
msg['To'] = 'dtechnologyg215@gmail.com'
msg['Subject'] = subject
msg.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login('dtechnologyg215@gmail.com', 'umymrihcbnhocltk')
    smtp.sendmail('dtechnologyg215@gmail.com', 'dtechnologyg215@gmail.com', msg.as_string())