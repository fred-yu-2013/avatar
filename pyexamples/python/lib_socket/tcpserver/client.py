# -*- coding: utf-8 -*-

import socket
import sys

# HOST, PORT = "localhost", 9999
HOST, PORT = "testapi.paopaoyun.com", 18080
# data = " ".join(sys.argv[1:])
data = 'Data from client.'

# Create a lib_socket (SOCK_STREAM means a TCP lib_socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    print 'connected.'
    sock.sendall(data + "\n")

    # Receive data from the server and shut down
    received = sock.recv(1024)

    sock.sendall(data + "\n")
    received = sock.recv(1024)
finally:
    sock.close()

print "Sent:     {}".format(data)
print "Received: {}".format(received)