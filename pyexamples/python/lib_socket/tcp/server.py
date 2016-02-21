#encoding=utf-8

"""
服务端，持续接受客户端的请求，并回复数据。
"""

import socket
import select
import time


def start_server(address, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((address, port))
    s.listen(5)
    conns = []
    print 'Server started at %s.' % repr((address, port))
    while True:
        read_list = [s]
        read_list.extend(conns)
        read_result, _, _ = select.select(read_list, [], [])
        for c in read_result:
            if c is s:
                conn, addr = s.accept()
                print 'Connected by', addr
                conn.setblocking(True)
                conns.append(conn)
            else:
                try:
                    data = c.recv(1024)
                    if not data:  # Empty means client has broken.
                        print 'Client has broken with EOF.'
                        c.close()
                        conns.remove(c)
                    else:
                        print 'RECV:', data
                        data = 'Server reply.'
                        c.send(data)
                        print 'SEND:', data
                except socket.error, socket.timeout:  # Client has stopped.
                    print 'Client has broken with lib_socket error or timeout.'
                    c.close()
                    conns.remove(c)

if __name__ == '__main__':
    start_server('127.0.0.1', 8200)
