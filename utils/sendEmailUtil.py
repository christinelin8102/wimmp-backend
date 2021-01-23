# -*- coding: utf-8 -*-
import smtplib
import os
from concurrent.futures import ThreadPoolExecutor
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
'''
   We have to write the email log info into database. however, there is no flask app context that we can 
utilize the Flask-SQLAlchemy session. So We have to use native SQLAlchemy object to create database 
record. another consideration is that we are under multi-threading environment, so we need to get a thread-
safe session to ensure our operation not damage data.
'''
EMAIL_SMTP_PORT = os.getenv('EMAIL_SMTP_PORT', '')
EMAIL_SMTP_SERVER = os.getenv('EMAIL_SMTP_SERVER', '')
EMAIL_SMTP_PORT_USER_NAME = os.getenv('EMAIL_SMTP_PORT_USER_NAME', None)
EMAIL_SMTP_PORT_USER_PASSWORD = os.getenv('EMAIL_SMTP_PORT_USER_PASSWORD', None)
EMAIL_SENDER_NAME = 'rd.test@wiadvance.com'


def sendNewEmail(sender, receiver, subject, content):
    try:
        msgRoot = MIMEMultipart('alternative')
        msgRoot['From'] = sender
        msgRoot['To'] = receiver
        msgRoot['Subject'] = subject
        msgText = MIMEText(content, 'html')
        msgRoot.attach(msgText)
        server = smtplib.SMTP(EMAIL_SMTP_SERVER)

        if EMAIL_SMTP_PORT_USER_PASSWORD is None:
            server.sendmail(sender, receiver, msgRoot.as_string())
        else:
            server.connect(EMAIL_SMTP_SERVER)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(EMAIL_SMTP_PORT_USER_NAME, EMAIL_SMTP_PORT_USER_PASSWORD)
            server.sendmail(sender, receiver, msgRoot.as_string())
        server.quit()
        print("Email Send")
        return "ok"
    except Exception as exc:
        # saveEmailLog(str(exc), sdtype, receiver, 0)
        return "error"


class SendEmail:

    @staticmethod
    def send(email, token, language, host_url, id):
        receiver = email
        filename = 'Creat_' + language + '.html'
        if language == 'tw':
            title = '數位戰情室系統 帳戶建立'
        elif language == 'cn':
            title = '數位戰情室系統 账户建立'
        else:
            title = 'GSQM War Room Account Create'

        filepath = './static/MailTemplate/' + filename
        html = open(filepath, 'r', encoding='UTF-8')
        htmlStr = html.read()
        htmlStr = htmlStr.replace('{domin}', host_url)
        htmlStr = htmlStr.replace('{receiver}', email)
        htmlStr = htmlStr.replace('{userId}', str(id))
        htmlStr = htmlStr.replace('{receiver}', email)
        htmlStr = htmlStr.replace('{token}', token)
        executor = ThreadPoolExecutor()
        executor.submit(sendNewEmail, EMAIL_SENDER_NAME, receiver, title, htmlStr)
        return "ok"
