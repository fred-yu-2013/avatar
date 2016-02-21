#encoding=utf-8

"""
支持持续连接服务端，并持续发送、接收数据。
"""

import socket
import time


def start_client(address, port):
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((address, port))
            while True:
                # Send and receiver data.
                data = 'Client request.'
                s.send(data)
                print 'SEND:', data
                data = s.recv(1024)
                print 'RECV:', data
                time.sleep(2)
        except socket.error, socket.timeout:
            print 'Socket error or timeout, try again later.'
            s.close()

        time.sleep(5)

if __name__ == '__main__':
    start_client('127.0.0.1', 8200)
