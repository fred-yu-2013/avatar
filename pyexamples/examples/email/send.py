# -*- coding: utf-8 -*-

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
# fp = open(textfile, 'rb')
# # Create a textplain message
# msg = MIMEText(fp.read())
msg = MIMEText('Hell from python.')
# fp.close()
# msg = 'Hell from pytho.'

# me == the sender's email address
me = 'chentj070921@yeah.net'
# you == the recipient's email address
you = 'chentj070921@yeah.net'
msg['Subject'] = '来自python的邮件'
msg['From'] = me
msg['To'] = you

# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP('smtp.yeah.net')
s.sendmail(me, [you], msg.as_string())
s.quit()
