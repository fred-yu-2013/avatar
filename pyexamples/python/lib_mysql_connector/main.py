# -*- coding: utf-8 -*-

# import mysql.connector
from mysql import connector

cnx = connector.connect(user='root', password='123456',
                              host='127.0.0.1',
                              database='dym_weixin_test')

cursor = cnx.cursor(dictionary=True)

cursor.execute("select * from film;")

rows = cursor.fetchall()
print rows
for row in rows:
    print row['id']

cnx.close()
