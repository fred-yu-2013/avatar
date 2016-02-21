__author__ = 'Fred'

import sqlite3

conn = sqlite3.connect(r'd:\CloudBackup.db', check_same_thread=False)
cursor = conn.cursor()
rows = cursor.execute('SELECT * FROM table_7C249FD1249F8CB0')
# rows = cursor.fetchall()
# try:
for row in rows:
    print row
# except:
#     pass

# q_str = u'''insert into table_7C249FD1249F8CB0 (id,
#                         requestid,
#                         path,
#                         type,
#                         level,
#                         size,
#                         md5,
#                         backupat,
#                         baidupcscode,
#                         baidupcsmd5,
#                         baidupcsfsid,
#                         baidupcspath,
#                         baidupcssize)
#         values (NULL,?,?,?,?,?,?,?,?,?,?,?,?)'''
# cursor.execute(q_str, (u'bce172ab-c05b-11e3-ab48-a733eaa65c49', u'/Baiduyun/1003files/dns/ProfileFunc.pyc', u'f', 4, 50894, u'c790b6a43a760b88686db605544e1a60', 1397099165.052157, 0, u'c790b6a43a760b88686db605544e1a60', 552318085985072L, u'/apps/ElastosBox/Box-6CA1110B4F10E8B2/1003files/dns/ProfileFunc.pyc', 50894))
#
# rows = cursor.execute('''SELECT * FROM table_7C249FD1249F8CB0 where requestid == 'bce172ab-c05b-11e3-ab48-a733eaa65c49'
#                             and path == '/Baiduyun/1003files/dns/ProfileFunc.pyc'
#                       ''')
# for row in rows:
#     print row