__author__ = 'Fred'

import sqlite3
import threading

connection = sqlite3.connect('storage.db', check_same_thread=False)


def thread_main():
    c = connection.cursor()
    for row in c.execute('SELECT * FROM stocks ORDER BY price'):
        print row


def main():
    c = connection.cursor()

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS stocks
                 (date text, trans text, symbol text, qty real, price real)''')

    # Insert a row of data
    c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

    # Save (commit) the changes
    connection.commit()

    for i in range(5):
        thread = threading.Thread(target=thread_main, args=())
        thread.start()

main()
