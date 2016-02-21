# -*- coding: utf-8 -*-
import imaplib
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import base64


def send_email_hello():
    sender = '793397089@qq.com'
    receiver = 'yufei.chen@dymfilm.com'
    subject = 'python email test'
    smtpserver = 'smtp.qq.com'
    username = '793397089@qq.com'
    password = base64.b64decode('eWYxMjE4eWoxMTA1')

    msg = MIMEText('你好', 'plain', 'utf-8')  # 内容
    msg['Subject'] = Header(subject, 'utf-8')  # 标题

    smtp = smtplib.SMTP_SSL()  # 需要SSL方式连接
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()


def my_unicode(s, encoding):
    if encoding:
        return unicode(s, encoding)
    else:
        return unicode(s)


class Email:
    def __init__(self, server, mid):
        self.server = server
        self.mid = mid
        self.sender = None
        self.receiver = None
        self.subject = None
        self.date = None

    def parse(self, data):
        msg = smtplib.email.message_from_string(data[0][1])
        self.sender = msg["From"]
        subject = smtplib.email.Header.decode_header(msg["Subject"])
        self.subject = self.to_utf8_str(subject[0][0], subject[0][1])

    def set_read(self):
        self.server.store(self.mid, '+FLAGS', '\Seen')

    def to_utf8_str(self, src, encoding):
        return src

    @property
    def command(self):
        return self.subject


def get_emails():
    pop = imaplib.IMAP4_SSL('pop.qq.com')
    pop.login('yufei.chen@dymfilm.com', base64.b64decode('ZlJlZDc5MzM5NzA4OQ=='))
    pop.select()  # 选择一个文件夹。比如收件箱，应该是有个协议的
    resp, items = pop.search(None, "Unseen")
    for item in items[0].split(' '):
        resp, mailData = pop.fetch(item, "(RFC822)")
        msg = smtplib.email.message_from_string(mailData[0][1])
        ls = msg["From"].split(' ')
        strfrom = ''
        if(len(ls) == 2):
           fromname = smtplib.email.Header.decode_header((ls[0]).strip('\"'))
           strfrom = 'From : ' + my_unicode(fromname[0][0], fromname[0][1]) + ls[1]
        else:
           strfrom = 'From : ' + msg["From"]
        strdate = 'Date : ' + msg["Date"]
        subject = smtplib.email.Header.decode_header(msg["Subject"])
        sub = my_unicode(subject[0][0], subject[0][1])
        strsub = 'Subject : ' + sub

        # 设置为已读，形如：'112', '112, 114'
        # pop.store(item, '+FLAGS', '\Seen')
        break


def get_emails2():
    server = imaplib.IMAP4_SSL('pop.qq.com')
    server.login('yufei.chen@dymfilm.com', base64.b64decode('ZlJlZDc5MzM5NzA4OQ=='))
    server.select()  # 选择一个文件夹。比如收件箱，应该是有个协议的
    resp, items = server.search(None, "Unseen")
    if resp != 'OK':
        return

    for item in items[0].split(' '):
        resp, mail_data = server.fetch(item, "(RFC822)")
        if resp != 'OK':
            return

        email = Email(server, item)
        email.parse(mail_data)
        email.set_read()
        break

if __name__ == '__main__':
    # send_email_hello()
    # get_emails()
    get_emails2()
