# -*- coding: utf-8 -*-
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# 设置smtplib所需的参数
# 下面的发件人，收件人是用于邮件传输的。
smtpserver = 'smtp.exmail.qq.com'
username = 'crm@medjaden.com'
password = 'Mjd@2019'
sender = 'crm@medjaden.com'


class EmailSender():

    def __init__(self, receiver, subject, ):
        '''
        初始化邮件发送对象
        :param receiver: 收件人：list 类型-['xxx@163.com','xxxx@qq.com']
        :param subject: 邮件标题
        '''
        self.receiver = receiver
        self.msg = MIMEMultipart('mixed')
        # 下面的主题，发件人，收件人，日期是显示在邮件页面上的。
        self.msg['Subject'] = subject
        self.msg['From'] = '{} <{}>'.format(username, username)
        # 收件人为多个收件人,通过join将列表转换为以;为间隔的字符串
        self.msg['To'] = ";".join(receiver)
        self.msg['Date'] = '{}'.format(datetime.datetime.now())

    def add_text(self, text_plain):
        '''
        构造文字内容
        :param text_plain: 字符串文件 可以使用回车换行等符号
        :return:
        '''
        text_plain = MIMEText(text_plain, 'plain', 'utf-8')
        self.msg.attach(text_plain)

    def add_img(self, img_name, sendimagefile):
        '''
        发送图片
        示例:
            sendimagefile = open(img_path, 'rb').read()
            send_img('ima_name',sendimagefile)
        :param imgname: 图片路径
        :return:
        '''

        image = MIMEImage(sendimagefile)
        image.add_header('Content-ID', '<image1>')
        image["Content-Disposition"] = 'attachment; filename="{}"'.format(img_name)
        self.msg.attach(image)

    def add_html(self, html):
        '''
        发送html
        :param html: html文件
        :return:
        '''
        text_html = MIMEText(html, 'html', 'utf-8')
        text_html["Content-Disposition"] = 'attachment; filename="texthtml.html"'
        self.msg.attach(text_html)

    def add_file(self, filename, sendfile):
        '''
        发送附件
            调用示例：
                    sendfile = open(r'xxxx.xls', 'rb').read()
                    add_file('file_name',sendfile)
        :param filename: 附件名称
        :param sendfile: 附件文件
        :return:
        '''
        # 构造附件
        text_att = MIMEText(sendfile, 'base64', 'utf-8')
        text_att["Content-Type"] = 'application/octet-stream'
        # 以下附件可以重命名成aaa.txt
        # text_att["Content-Disposition"] = 'attachment; filename="aaa.txt"'
        # 另一种实现方式
        text_att.add_header('Content-Disposition', 'attachment', filename=filename)
        # 以下中文测试不ok
        # text_att["Content-Disposition"] = u'attachment; filename="中文附件.txt"'.decode('utf-8')
        self.msg.attach(text_att)

    def send(self):
        # 发送邮件
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)
        # 我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
        # smtp.set_debuglevel(1)
        smtp.login(username, password)
        smtp.sendmail(sender, self.receiver, self.msg.as_string())
        smtp.quit()


if __name__ == '__main__':
    em_obj = EmailSender(['80921970@qq.com'],'测试邮件')
    em_obj.add_text('测试邮件发送代码，无需回复')
    em_obj.send()
