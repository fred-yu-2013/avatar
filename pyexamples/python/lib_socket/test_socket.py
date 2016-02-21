#coding=utf-8

import socket
import select


'''
演示了socket的使用，可以一个server对多个client。
'''

HOST = '127.0.0.1'
PORT = 8100


def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)
    conns = []
    print 'Server started.'
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
                    print 'From connection.', repr(data)
                    if data:
                        print 'RECV:', data
                        data = 'Server reply.'
                        c.send(data)
                        print 'SEND:', data
                    else:  # Empty data means EOF of the lib_socket.
                        print 'Client has broken with EOF.'
                        c.close()
                        conns.remove(c)
                except socket.error, socket.timeout:  # Client has stopped.
                    print 'Client has broken with lib_socket.error.'
                    c.close()
                    conns.remove(c)


def start_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    data = 'Client request.'
    s.send(data)
    print 'SEND:', data
    data = s.recv(1024)
    print 'RECV:', data
    while True:
        data = s.recv(1024)
        print 'After recv.'

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'client':
        start_client()
    else:
        start_server()

